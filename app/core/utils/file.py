import json
import os
import shutil
from typing import Any, Iterator

import yaml
from app.core.utils import json_helper


def check_directory(filepath: str, create_directories: bool = False):
    directory = os.path.dirname(filepath)
    if not os.path.isdir(directory):
        if os.path.exists(directory):
            raise Exception(f"File {directory} already exists and isn't a directory.")
        if create_directories:
            os.makedirs(directory)


def write_text_file(
    filepath: str, text: str, encoding: str = "utf-8", create_directories: bool = False
) -> None:
    check_directory(filepath, create_directories)
    with open(filepath, encoding=encoding, mode="wt") as file:
        file.write(text)


def append_text_file(filepath: str, text: str, encoding: str = "utf-8") -> None:
    with open(filepath, encoding=encoding, mode="at") as file:
        file.write(text)


def write_new_text_file(filepath: str, text: str, encoding: str = "utf-8") -> None:
    with open(filepath, encoding=encoding, mode="xt") as file:
        file.write(text)


def write_json_file(
    filepath: str, content: Any, pretty: bool = False, create_directories: bool = False
) -> None:
    check_directory(filepath, create_directories)
    with open(filepath, encoding="utf-8", mode="wt") as file:
        if pretty:
            json.dump(content, file, indent=4, cls=json_helper.DASJSONEncoder)
        else:
            json.dump(content, file, cls=json_helper.DASJSONEncoder)


def write_new_json_file(filepath: str, content: Any, pretty: bool = False) -> None:
    with open(filepath, encoding="utf-8", mode="xt") as file:
        if pretty:
            json.dump(content, file, indent=4, cls=json_helper.DASJSONEncoder)
        else:
            json.dump(content, file, cls=json_helper.DASJSONEncoder)


def append_json_line_file(filepath: str, content: Any) -> None:
    with open(filepath, encoding="utf-8", mode="at") as file:
        json.dump(content, file, separators=(",", ":"), cls=json_helper.DASJSONEncoder)
        file.write("\n")


def read_json_file(filepath: str) -> Any:
    with open(filepath, encoding="utf-8", mode="rt") as file:
        return json.load(file)


def read_json_lines_file(filepath: str) -> Iterator[Any]:
    for line in read_lines_file(filepath, encoding="utf-8"):
        yield json.loads(line)


def read_text_file(filepath: str, encoding: str = "utf-8") -> str:
    with open(filepath, encoding=encoding, mode="rt") as file:
        return file.read()


def read_text_file_lines(filepath: str, encoding: str = "utf-8") -> list[str]:
    with open(filepath, encoding=encoding, mode="rt") as file:
        return file.readlines()


def read_lines_file(filepath: str, encoding: str = "utf-8") -> Iterator[str]:
    with open(filepath, encoding=encoding, mode="rt") as file:
        for line in file.readlines():
            yield line


def read_bytes_file(filepath: str) -> bytes:
    with open(filepath, mode="rb") as file:
        return file.read()


def read_yaml_file(filepath: str) -> Any:
    with open(filepath, encoding="utf-8", mode="rt") as file:
        return yaml.safe_load(file)


def create_empty_dir(dir_path: str):
    """
    Create an empty directory at the provided path.
    Warning ! If the folder exists, it is deleted with its contents.
    """
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
    else:
        os.mkdir(dir_path)


def dirs_with_files(dir_path: str, min_file_count: int = 0) -> list[str]:
    """
    Recursive listing of the directories within a given directory, for which there are at least n files
    """
    return [
        root for root, dirs, files in os.walk(dir_path) if len(files) > min_file_count
    ]

