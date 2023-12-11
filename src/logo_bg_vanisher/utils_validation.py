"""
Module to handle user validation
"""
from typing import Tuple


def is_string_valid(text: str) -> str:
    """
    Validates if text is string
    :param text:
    :return: str
    """
    if not isinstance(text, str):
        raise ValueError("Input must be string!")
    return text


def are_numbers_valid(*args) -> Tuple[int, ...]:
    """
    Validates that all provided arguments are integers.

    :param args: A variable number of arguments.
    :return: Tuple of the provided integers.
    :raises ValueError: If no arguments are provided or if any argument is not an integer.
    """
    if not args:
        raise ValueError("No arguments provided!")

    items = []
    for item in args:
        if not isinstance(item, int):
            raise ValueError(f"Wrong type {type(item)}. Expected int")
        items.append(item)
    return tuple(items)
