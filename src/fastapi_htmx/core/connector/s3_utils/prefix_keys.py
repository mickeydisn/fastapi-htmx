import os
from pathlib import Path
from typing import Any, Optional

from botocore.paginate import PageIterator

from fastapi_htmx.core.connector.s3_utils.normalise_prefix import normalise_prefix
from fastapi_htmx.datahub.utils.custom_logger import DatahubLogger

_log = DatahubLogger(Path(__file__).stem)

__all__ = ["PrefixKeys"]


class PrefixKeys:
    def __init__(
        self,
        page_iterator: Optional[PageIterator],
        prefix: str,
        recursive: bool,
        ignore_extensions: list[str],
        allowed_extensions: list[str],
        obj_key: Optional[str],
        files_only: bool,
        directory_only: bool,
    ):
        self.page_iterator = page_iterator
        self.prefix = prefix
        self.recursive = recursive
        self.ignore_extensions = ignore_extensions
        self.allowed_extensions = allowed_extensions
        self.obj_key = obj_key
        self.files_only = files_only
        self.directory_only = directory_only

        _log.debug(
            f"{self.prefix=}, {self.recursive=}, {self.ignore_extensions=}, "
            f"{self.allowed_extensions=}, {self.obj_key=}, "
            f"{self.files_only=}, {self.directory_only=}"
        )

        if files_only and directory_only:
            raise Exception("Cannot set both files_only=True and directory_only=True")

        if directory_only:
            if ignore_extensions:
                raise Exception("ignore_extensions is only valid when files_only=True")
            if allowed_extensions:
                raise Exception("allowed_extensions is only valid when files_only=True")
            if obj_key != "Key":
                raise Exception(
                    "When directory_only=True, obj_key must be 'Key' to extract directories correctly"
                )

        if (
            files_only
            and ignore_extensions
            and sorted(ignore_extensions) == sorted(allowed_extensions)
        ):
            raise Exception(
                "ignore_extensions and allowed_extensions cannot be identical when files_only=True"
            )

    def __call__(self):
        return self.process_page_iterator()

    def process_page_iterator(self) -> list[Any]:
        if self.page_iterator is None:
            raise Exception("page_iterator must not be None")

        objs = []
        for page in self.page_iterator:
            if "Contents" in page:
                objs.extend(self.process_contents(page["Contents"]))
        return objs

    def process_contents(self, page_contents: list[Any]) -> list[Any]:
        objs = []

        for obj in page_contents:
            key = obj["Key"]
            _log.debug(f"{key=}")

            if self.recursive:
                if not self.key_within_prefix(self.prefix, key):
                    continue
            else:
                if not self.key_within_init_prefix_level(self.prefix, key):
                    continue

            valid_keys = self.is_valid_key(key)
            if valid_keys:
                if self.files_only:
                    result = [obj] if self.obj_key is None else [obj[self.obj_key]]
                else:
                    result = valid_keys
                objs.extend(result)

        if self.obj_key == "Key" and not self.files_only:
            objs = list(set(objs))  # Deduplicate
        return objs

    def is_valid_key(self, key: str) -> list[str]:
        if self.key_id_directory(key):
            _log.debug(f"Directory identified: {key}")
            if self.directory_only or not self.files_only:
                return [key]
            return []

        if self.directory_only:
            return [f"{os.path.dirname(key)}/"]

        extension = os.path.splitext(key)[1]
        if extension in self.ignore_extensions:
            return []

        if not self.allowed_extensions:
            return [key, f"{os.path.dirname(key)}/"]

        if extension not in self.allowed_extensions:
            return []

        return [key, f"{os.path.dirname(key)}/"]

    @staticmethod
    def key_within_prefix(_prefix: str, key: str) -> bool:
        _prefix = normalise_prefix(_prefix, end_slash=True)
        _log.debug(f"Checking prefix match: {key=} starts with {_prefix=}")
        return _prefix == "/" or (key.startswith(_prefix) and key != _prefix)

    @staticmethod
    def key_id_directory(key: str) -> bool:
        return key.endswith("/")

    @staticmethod
    def key_within_init_prefix_level(prefix: str, key: str) -> bool:
        norm_prefix = normalise_prefix(prefix)
        norm_key = normalise_prefix(key)

        if not norm_prefix:
            return norm_key.count("/") == 0

        norm_prefix = f"{norm_prefix}/"
        if not norm_key.startswith(norm_prefix):
            return False

        return norm_key[len(norm_prefix):].count("/") == 0


if __name__ == "__main__":
    import datetime
    from dateutil.tz import tzutc

    base_page_contents = [
        {"Key": "test.parquet", "LastModified": datetime.datetime(2024, 7, 30, 14, 19, 15, 669000, tzinfo=tzutc()), "ETag": '"xxx"', "Size": 0, "StorageClass": "STANDARD"},
        {"Key": "test.txt", "LastModified": datetime.datetime(2024, 7, 30, 14, 19, 15, 669000, tzinfo=tzutc()), "ETag": '"xxx"', "Size": 0, "StorageClass": "STANDARD"},
        {"Key": "dir1/", "LastModified": datetime.datetime(2024, 7, 30, 14, 19, 15, 669000, tzinfo=tzutc()), "ETag": '"xxx"', "Size": 0, "StorageClass": "STANDARD"},
        {"Key": "dir1/test.parquet", "LastModified": datetime.datetime(2024, 7, 30, 14, 19, 15, 669000, tzinfo=tzutc()), "ETag": '"xxx"', "Size": 0, "StorageClass": "STANDARD"},
        {"Key": "dir1/test.txt", "LastModified": datetime.datetime(2024, 7, 30, 14, 19, 15, 669000, tzinfo=tzutc()), "ETag": '"xxx"', "Size": 0, "StorageClass": "STANDARD"},
        {"Key": "dir1/dir2/", "LastModified": datetime.datetime(2024, 7, 30, 14, 19, 15, 669000, tzinfo=tzutc()), "ETag": '"xxx"', "Size": 0, "StorageClass": "STANDARD"},
        {"Key": "dir1/dir2/test.parquet", "LastModified": datetime.datetime(2024, 7, 30, 14, 19, 18, 892000, tzinfo=tzutc()), "ETag": '"xxx"', "Size": 48946, "StorageClass": "STANDARD"},
        {"Key": "dir1/dir2/test.txt", "LastModified": datetime.datetime(2024, 7, 30, 14, 19, 18, 892000, tzinfo=tzutc()), "ETag": '"xxx"', "Size": 48946, "StorageClass": "STANDARD"},
    ]

    args_ = {
        "prefix": "",
        "recursive": True,
        "ignore_extensions": [],
        "allowed_extensions": [],
        "obj_key": "Key",
        "files_only": False,
        "directory_only": True,
        "page_iterator": None,
    }

    c = PrefixKeys(**args_)
    print(c.process_contents(base_page_contents))
