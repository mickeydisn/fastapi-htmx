import random
from typing import Optional, Final


def rand_int(min_int: int = 0, max_int: int = 900_000_000) -> int:
    return random.randint(min_int, max_int)


def mb_to_byte(size_in_mb: int) -> int:
    return size_in_mb * 1024 * 1024


def apply_factor(number: int, factor: float) -> int:
    """
    Applying a factor to a given int and returns an int.
    @return: int
    """
    return int(number * factor)


class ByteSizes:
    KB: Final[int] = 1024
    MB: Final[int] = KB**2
    GB: Final[int] = KB**3

    @staticmethod
    def kilo(size: int) -> int:
        return size * ByteSizes.KB

    @staticmethod
    def to_kilo(size: int) -> float:
        return size / ByteSizes.KB

    @staticmethod
    def to_kilo_int(size: int) -> int:
        return size // ByteSizes.KB

    @staticmethod
    def mega(size: int) -> int:
        return size * ByteSizes.MB

    @staticmethod
    def to_mega(size: int) -> float:
        return size / ByteSizes.MB

    @staticmethod
    def to_mega_int(size: int) -> int:
        return size // ByteSizes.MB

    @staticmethod
    def giga(size: int) -> int:
        return size * ByteSizes.GB

    @staticmethod
    def to_giga(size: int) -> float:
        return size / ByteSizes.GB

    @staticmethod
    def to_giga_int(size: int) -> int:
        return size // ByteSizes.GB


def join(
    elements: Optional[list], sep: str = ", ", prefix: str = "", postfix: str = ""
) -> str:
    if elements is None or len(elements) == 0:
        return ""
    return f"{prefix}{sep.join(elements)}{postfix}"


def str_to_bool(value: str) -> bool:
    return value.lower() == "true"


def flatten_list_of_list(input_list) -> list:
    """
    Flatten list of lists
    """

    def walk(e):
        if isinstance(e, list):
            for v2 in e:
                for v3 in walk(v2):
                    yield v3
        else:
            yield e

    return [v for v in walk(input_list)]
