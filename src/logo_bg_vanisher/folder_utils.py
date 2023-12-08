"""
Module to handle file operations
"""
import os
from pathlib import Path
from typing import List
from typing import Tuple
from typing import Union

from PIL.Image import Image

from .image_creator import CreatePillowImage


def find_files(path: Path, extension: Union[str, Tuple, None]) -> List[Path]:
    """
    Finds and returns files with certain extension
    :param path:
    :param extension:
    :return:
    """
    if extension:
        return [pic for pic in path.iterdir() if pic.suffix in extension]
    else:
        return [pic for pic in path.iterdir()]


def load_image(picture: Path) -> Union[Image, None]:
    try:
        if not picture.exists():
            raise ValueError('The picture could not be found!')
        if not os.access(picture, os.R_OK):
            raise PermissionError(f"Permission denied for file {picture} !")
        if picture:
            image_creator = CreatePillowImage()
            image_obj = image_creator.convert_image(file=picture)
            return image_obj
    except PermissionError as exc:
        raise PermissionError(f"Permission error: {exc}") from exc
    except OSError as exc:
        raise OSError(f"Error opening image: {exc}") from exc
