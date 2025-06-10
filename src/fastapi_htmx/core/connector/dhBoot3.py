
import io
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Optional, Any, Final, List, AnyStr
from typing import List, Dict, Union


import boto3
from boto3.s3.transfer import TransferConfig

from fastapi_htmx.config.constants import (
    DEFAULT_S3_PROVIDER,
    DEFAULT_S3_SERVICE_NAME,
    DAS_PERSISTENT_FOLDER,
)

from fastapi_htmx.config.configClass import DAConfig


from fastapi_htmx.core.connector.s3_utils.normalise_prefix import normalise_prefix
from fastapi_htmx.core.connector.s3_utils.prefix_keys import PrefixKeys
from fastapi_htmx.core.utils.miscellaneous import ByteSizes


class DhBoto3:
    def __init__(
        self,
        provider: Optional[str] = None,
        customised_provider_credentials: Optional[dict[str, str]] = None,
    ):
        self.provider: Final[Optional[str]] = provider
        self.customised_provider_credentials: Final[
            Optional[Optional[dict[str, str]]]
        ] = customised_provider_credentials
        self.client = self.get_client(provider, customised_provider_credentials)

    @staticmethod
    def get_client(
        provider: Optional[str] = None,
        customised_client: Optional[dict[str, str]] = None,
    ):
        if customised_client is None and provider is not None:
            provider_config = DAConfig.S3_CONFIG(provider)
        elif provider is None and customised_client is not None:
            provider_config = customised_client
        else:
            # default provider
            provider_config = DAConfig.S3_CONFIG(DEFAULT_S3_PROVIDER)
        provider_config = {"service_name": DEFAULT_S3_SERVICE_NAME} | provider_config


        try:
            return boto3.client(**provider_config)
        except Exception as e:
            raise Exception(f"boto3 connection failed: {e}")

    def get_buckets(self) -> list[str]:
        """
        Return a list of bucket names under current S3 client
        """
        buckets = self.client.list_buckets()["Buckets"]
        return [bucket["Name"] for bucket in buckets]


    def list_one_level_objects(
        self,
        bucket: str,
        prefix: str = "",
        delimiter: str = "/",
        include_directories: bool = True,
        include_files: bool = True,
        depth = 0
    ) -> List[Dict[str, Union[str, int]]]:
        result = []
        # prefix = normalise_prefix(prefix)  # Make sure it ends with "/"

        print ('prefix:', prefix)

        paginator = self.client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix, Delimiter=delimiter):
            # Handle files directly under the prefix
            if include_files and "Contents" in page:
                for obj in page["Contents"]:
                    if obj["Key"] == prefix:
                        continue  # skip the folder object itself
                    result.append({
                        "path": obj["Key"],
                        "size": obj["Size"],
                        "type": "file"
                    })

            # Handle subdirectories (CommonPrefixes)
            if include_directories and "CommonPrefixes" in page:
                for cp in page["CommonPrefixes"]:

                    if depth > 0:
                        result += self.list_one_level_objects(bucket, cp["Prefix"], delimiter, depth=depth - 1)
                    else:
                        result.append({
                            "path": cp["Prefix"],
                            "size": 0,
                            "type": "directory"
                        })


        return result

    def list_all_objects(
        self,
        bucket: str,
        prefix: str = "",
        include_directories: bool = True,
        include_files: bool = True
    ) -> List[Dict[str, Union[str, int]]]:
        result = []
        paginator = self.client.get_paginator("list_objects_v2")
        prefix = normalise_prefix(prefix)  # ensure it ends with "/" if it's a folder

        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):  # <-- NO Delimiter!
            if "Contents" in page:
                for obj in page["Contents"]:
                    if obj["Key"] == prefix and obj["Size"] == 0:
                        continue

                    entry = {
                        "path": obj["Key"],
                        "size": obj["Size"],
                        "type": "file" if not obj["Key"].endswith("/") else "directory"
                    }

                    if entry["type"] == "file" and include_files:
                        result.append(entry)
                    elif entry["type"] == "directory" and include_directories:
                        result.append(entry)

        return result


    def prefix_keys(
        self,
        bucket: str,
        prefix: str,
        max_keys: int = 1000,
        recursive: bool = False,
        ignore_extensions: Optional[list[str]] = None,
        allowed_extensions: Optional[list[str]] = None,
        obj_key: Optional[str] = None,
        files_only: bool = False,
        directory_only: bool = False,
    ) -> List[Any]:
        """
        @param bucket:
        @param prefix: Eg. 2024/02/01
        @param max_keys:
        @param recursive:
        @param ignore_extensions:
        @param allowed_extensions:
        @param obj_key: only returns the value of the key provided
        @param files_only: only returns
        @param directory_only: only returns the directories under the given prefix
        @return: list of bucket information
        Notes:
            - Only directories with files within them at 1st to n levels will be listed.
        """
        norm_prefix = normalise_prefix(prefix)
        paginator = self.client.get_paginator("list_objects_v2")
        page_iterator = paginator.paginate(
            Bucket=bucket,
            Prefix=norm_prefix,
            MaxKeys=max_keys,
        )
        ignore_extensions = list() if not ignore_extensions else ignore_extensions
        allowed_extensions = list() if not allowed_extensions else allowed_extensions
        return PrefixKeys(
            page_iterator,
            norm_prefix,
            recursive,
            ignore_extensions,
            allowed_extensions,
            obj_key,
            files_only,
            directory_only,
        )()

    def download_key(
        self,
        bucket_name: str,
        s3_file_path: str,
        local_file_path: str,
        multipart_chunksize: int = 8,
        max_concurrency: int = 10,
        max_bandwidth: int = 10 * 8,
    ) -> bool:
        """
        Download of a single file to S3 bucket

        @param bucket_name:
        @param s3_file_path:
        @param local_file_path:
        @param multipart_chunksize: default 8 MB chuck size per multipart download
        @param max_concurrency: default 10 multipart downloads
        @param max_bandwidth: default 8 MB * 10 per sec (from default part size is 8 MB and 10 of max concurrency)
        @return:
        """
        try:
            self.client.download_file(
                bucket_name,
                s3_file_path,
                local_file_path,
                Config=TransferConfig(
                    multipart_chunksize=multipart_chunksize * ByteSizes.MB,
                    max_concurrency=max_concurrency,
                    max_bandwidth=max_bandwidth * ByteSizes.MB,
                ),
            )
            return True
        except Exception as e:
            log.error({"comment": f"Failed download_key {e}"})
            return False

    def download_keys(
        self,
        bucket_name: str,
        s3_prefix: str,
        s3_file_names: list | None = None,
        local_path: AnyStr | None = None,
        limit: Optional[int] = None,
        max_threads: int = 10,
        multipart_chunksize: int = 8,
        max_concurrency: int = 10,
        max_bandwidth: int = 10 * 8,
    ) -> bool:
        """
        Download all files under a specific folder on S3

        @param bucket_name: Bucket where to find files to download
        @param s3_prefix: Path inside the bucket (directories only)
        @param s3_file_names: specific list of file names to download from the s3 folder
        @param local_path: local path where to store the downloaded files
        @param limit: limit download keys (if defined)
        @param max_threads: thread pool size for concurrent boto3 download function execution
        @param multipart_chunksize: default 8 MB chuck size per multipart downloads
        @param max_concurrency: default 10 multipart downloads
        @param max_bandwidth: default 8 MB * 10 per sec (from default part size is 8 MB and 10 of max concurrency)

        @return: True if files were downloaded successfully else False
        """
        root_folder = "downloads" if local_path is None else local_path
        if not os.path.exists(root_folder):
            os.makedirs(root_folder)

        if s3_file_names is None:
            # scan the S3 directory
            all_files_to_download = self.prefix_keys(
                bucket_name, s3_prefix, obj_key="Key", files_only=True
            )
        else:
            # list the full path of the S3 files dir/file_name.ext
            all_files_to_download = [f"{s3_prefix}/{x}" for x in s3_file_names]

        if limit:
            all_files_to_download = all_files_to_download[:limit]

        all_local_path = [
            os.path.join(root_folder, os.path.basename(x))
            for x in all_files_to_download
        ]

        # required for the thread "map"
        file_count = len(all_local_path)
        bucketList = [bucket_name] * file_count
        multipart_chunksize = [multipart_chunksize] * file_count
        max_concurrency = [max_concurrency] * file_count
        max_bandwidth = [max_bandwidth] * file_count

        try:
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                executor.map(
                    self.download_key,
                    bucketList,
                    all_files_to_download,
                    all_local_path,
                    multipart_chunksize,
                    max_concurrency,
                    max_bandwidth,
                )
        except Exception as e:
            log.error({"comment": f"S3 boto3 download failed, error : {e}"})
            return False
        return True

    def upload_data(
        self, s3_bucket: str, s3_path: str, data: bytearray | bytes
    ) -> bool:
        """
        Upload binary data to S3.
        """
        try:
            with io.BytesIO() as buffer_out:
                buffer_out.write(data)
                buffer_out.seek(0)
                self.client.upload_fileobj(buffer_out, s3_bucket, s3_path)
                return True
        except Exception as e:
            log.error(f"Failed to upload data to {s3_bucket} / {s3_path}: {e}")
            return False

    def touch(self, s3_bucket: str, s3_path: str) -> bool:
        """
        Touch a S3 path (create an empty file).
        """
        return self.upload_data(s3_bucket, s3_path, b"")

    def upload_file(
        self,
        bucket_name: str,
        s3_file_path: str,
        local_file_path: str,
        multipart_chunksize: int = 8,
        max_concurrency: int = 10,
        max_bandwidth: int = 10 * 8,
    ) -> bool:
        """
        Upload of a single file to S3 bucket

        @param bucket_name:
        @param s3_file_path: fulle path of the file on S3 (dir/file_name.ext)
        @param local_file_path:
        @param multipart_chunksize: default 8 MB chuck size per multipart upload
        @param max_concurrency: default 10 multipart uploads
        @param max_bandwidth: default 8 MB * 10 per sec (from default part size is 8 MB and 10 of max concurrency)
        @return:
        """
        try:
            self.client.upload_file(
                local_file_path,
                bucket_name,
                s3_file_path,
                Config=TransferConfig(
                    multipart_chunksize=multipart_chunksize * ByteSizes.MB,
                    max_concurrency=max_concurrency,
                    max_bandwidth=max_bandwidth * ByteSizes.MB,
                ),
            )
            return True
        except Exception as e:
            # a failure of a single upload cannot be caught and will result in data loss
            # so the solution is to save the file in error and upload it manually
            log.error(f"Failed upload_file {e}")
            uploadFailureFolder = (
                f'failedUpload_{datetime.now().strftime("%Y%m%d%H%M%S%f")}'
            )
            fName = os.path.basename(local_file_path)
            if das_deployed():
                # on container
                path = os.path.join(DAS_PERSISTENT_FOLDER, uploadFailureFolder, fName)
            else:
                # local
                path = os.path.join(DAConfig.TEMP_FOLDER, uploadFailureFolder, fName)
            if not os.path.exists(path):
                os.makedirs(path)
            shutil.copy(local_file_path, path)
            log.error(
                f"Failed uploaded file is stored in {path=}, upload it manually to "
                f"bucket={bucket_name}, S3 path={s3_file_path} !"
            )
            return False

    def upload_files(
        self,
        s3_bucket: str,
        s3_path: str,
        local_file_paths: list[str],
        max_threads: int = 10,
        multipart_chunksize: int = 8,
        max_concurrency: int = 10,
        max_bandwidth: int = 10 * 8,
    ) -> bool:
        """
        Upload n files to a S3 bucket directory.

        @param s3_bucket:
        @param s3_path: s3 path as directories
        @param local_file_paths: full local file paths
        @param max_threads: thread pool size for concurrent boto3 upload function execution
        @param multipart_chunksize: default 8 MB chuck size per multipart upload
        @param max_concurrency: default 10 multipart uploads
        @param max_bandwidth: default 8 MB * 10 per sec (from default part size is 8 MB and 10 of max concurrency)
        @return:
        """

        def make_s3_file_path(s3_path_: str, local_file_path: str) -> str:
            file_name = os.path.basename(local_file_path)
            if not s3_path_:
                file_prefix = file_name
            else:
                file_prefix = f"{s3_path_}/{file_name}"
            return file_prefix.replace("\\", "/")

        s3_file_paths = [make_s3_file_path(s3_path, x) for x in local_file_paths]

        # required for the thread "map"
        file_count = len(s3_file_paths)
        bucket_list = [s3_bucket] * file_count
        multipart_chunksize = [multipart_chunksize] * file_count
        max_concurrency = [max_concurrency] * file_count
        max_bandwidth = [max_bandwidth] * file_count

        try:
            with ThreadPoolExecutor(max_workers=max_threads) as executor:
                executor.map(
                    self.upload_file,
                    bucket_list,
                    s3_file_paths,
                    local_file_paths,
                    multipart_chunksize,
                    max_concurrency,
                    max_bandwidth,
                )
        except Exception as e:
            log.error({"comment": f"S3 boto3 upload failed, error : {e}"})
            return False
        return True

    def copy_key(
        self,
        origin_bucket: str,
        origin_key_path: str,
        dest_bucket: str,
        dest_key_path: str,
    ) -> bool:
        """
        Copy 1 file in a bucket to another bucket
        """
        try:
            copy_source = {"Bucket": origin_bucket, "Key": origin_key_path}
            self.client.copy(copy_source, dest_bucket, dest_key_path)
        except Exception as e:
            log.error(
                {
                    "comment": f"S3 copy file failed ({e}) - origin = {origin_bucket} {origin_key_path}; "
                    f"destination = {dest_bucket} {dest_key_path}"
                }
            )
            return False
        return True

    def copy_keys(
        self,
        origin_bucket: str,
        origin_key_path: list,
        dest_bucket: str,
        dest_key_path: list,
    ) -> bool:
        """
        Copy n keys.
        """
        all_copy_success = True
        for orig_key, dest_key in zip(origin_key_path, dest_key_path):
            copy_success = self.copy_key(origin_bucket, orig_key, dest_bucket, dest_key)
            if not copy_success:
                all_copy_success = False
        return all_copy_success

    def delete_key(self, bucket_name: str, s3_key: str) -> bool:
        """
        Deletion of a single S3 key.
        """
        response = self.client.delete_object(Bucket=bucket_name, Key=s3_key)
        if "Errors" in response:
            err_msg = response["Errors"]
            log.error(
                {
                    "comment": f"S3 file deletion failed ({err_msg}) for {bucket_name} {s3_key}"
                }
            )
            return False
        return True

    def delete_keys(
        self, bucket_name: str, s3_keys: list, max_keys: int = 1000
    ) -> bool:
        """
        Remove files inside a bucket, keys (files to remove) can be retrieved by using self.folder_keys function
        :bucket:bucket name
        :keys: files to remove
        """
        if not s3_keys:
            return True

        keys = list(set(s3_keys))
        key_slices = [keys[i : i + max_keys] for i in range(0, len(keys), max_keys)]

        # delete Keys
        for key_slice in key_slices:
            key_list = []
            for key in key_slice:
                key_list += [{"Key": key}]
            response = self.client.delete_objects(
                Bucket=bucket_name, Delete={"Objects": key_list}
            )
            deleted = [] if "Deleted" not in response else response["Deleted"]
            errors = [] if "Errors" not in response else response["Errors"]
            if len(deleted) != len(key_slice) or len(errors) > 0:
                log.error({"comment": f"S3 boto3 delete file failed, error : {errors}"})
                return False
        return True

    def delete_zero_byte_keys(
        self, bucket_name: str, prefix: str, ignore_extensions: list[str] = None
    ) -> bool:
        keys = self.prefix_keys(
            bucket_name, prefix, files_only=True, ignore_extensions=ignore_extensions
        )
        zero_byte_keys = [key_info["Key"] for key_info in keys if key_info["Size"] == 0]
        if zero_byte_keys:
            return self.delete_keys(bucket_name, zero_byte_keys)
        return True

    def delete_folder_keys(
        self, bucket_name: str, s3_folder: str, recursive: bool = False
    ) -> bool:
        """
        Deleting all the files contained in a given folder of a S3 bucket's folder.
        """
        s3_keys = self.prefix_keys(
            bucket_name, s3_folder, recursive=recursive, obj_key="Key", files_only=True
        )
        return self.delete_keys(bucket_name, s3_keys)

    def move_keys(
        self,
        origin_bucket: str,
        origin_key_path: list,
        dest_bucket: str,
        dest_key_path: list,
    ) -> bool:
        """
        Moving keys in S3 is a copy to the new key path and then a deletion of the old key.
        It is done here as a copy of n files and on success the deletion of n files.
        If the copy fails, the deletion is not carried out.
        """
        copy_success = self.copy_keys(
            origin_bucket, origin_key_path, dest_bucket, dest_key_path
        )
        if not copy_success:
            return False
        delete_success = self.delete_keys(origin_bucket, origin_key_path)
        if not delete_success:
            return False
        return True

    def copy(
        self,
        origin_bucket: str,
        origin_path: str,
        dest_bucket: str,
        dest_path: str,
        recursive: bool = False,
    ) -> bool:
        origin_keys = self.prefix_keys(
            origin_bucket,
            origin_path,
            recursive=recursive,
            obj_key="Key",
            files_only=True,
        )
        dest_keys = [x.replace(origin_path, dest_path) for x in origin_keys]
        success = self.copy_keys(origin_bucket, origin_keys, dest_bucket, dest_keys)
        return success

    def read_file(self, bucket: str, key_path: str, file_name: str) -> str:
        """
        To read files that can be read without special libraries (txt, json...).
        """
        file_path = f"{key_path}/{file_name}"
        data = self.client.get_object(Bucket=bucket, Key=file_path)
        return data["Body"].read().decode("utf-8")

    def __enter__(self) -> "DhBoto3":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if self.client:
            self.client.close()
            self.client = None

    def __del__(self):
        self.close()
