"""
Module which handles background removal from pics using Pillow
"""
from typing import Tuple

import PIL
from PIL import Image
from PIL import ImageFilter

from .background_remover import BackgroundRemovalStrategy


class PillowBackgroundRemoval(BackgroundRemovalStrategy):
    """
    Removes the background using the Pillow standard library.
    It identifies the first pixel (upper left), which is background, and not the logo itself.
    """

    def __init__(self, img: Image, tolerance: int = 50, edge_tolerance: int = 50):
        super().__init__(img)
        self.validate_image(image=img)
        self.tolerances = self.validate_tolerences(tolerance=tolerance, edge_tolerance=edge_tolerance)
        self.filename = img.filename
        self.tolerance = self.tolerances[0]
        self.edge_tolerance = self.tolerances[1]
        self.suffix = "pillow_converted"

    def remove_background(self) -> Image:
        if self.image is None or not hasattr(self.image, 'convert'):
            raise ValueError("Invalid image object provided")

        img = self.image.convert("RGBA")
        processed_img = self._process_image_data(img=img)
        processed_img.filename = self.filename
        return processed_img

    def _process_image_data(self, img: Image) -> list:
        # Get the background color (assuming it's the color of the top-left pixel)
        bg_color = img.getpixel((0, 0))
        # Convert img to grayscale for better edge detection and create an edge mask
        edge_mask = img.convert("L").filter(ImageFilter.FIND_EDGES)
        data = img.getdata()
        edge_data = edge_mask.getdata()
        new_data = []
        for i, item in enumerate(data):
            if edge_data[i] > 0:  # If the pixel is on an edge
                if all(abs(item[j] - bg_color[j]) <= self.edge_tolerance for j in range(3)):
                    new_data.append((255, 255, 255, 0))  # Transparent
                else:
                    new_data.append(item)
            else:
                if all(abs(item[j] - bg_color[j]) <= self.tolerance for j in range(3)):
                    new_data.append((255, 255, 255, 0))  # Transparent
                else:
                    new_data.append(item)
        img.putdata(new_data)
        return img

    @staticmethod
    def validate_image(image: Image) -> bool:
        """
        Validates the image object
        :param image: Image
        :return: bool
        """
        if not isinstance(image, Image.Image):
            raise ValueError(f"Provided object not of type {type(image)}")
        return True

    @staticmethod
    def validate_tolerences(tolerance: int, edge_tolerance: int) -> Tuple[int, int]:
        """
        Validates the tolerances
        :param tolerance: Background tolerance
        :param edge_tolerance: Edge tolerance
        :return: tolerance, edge_tolerance
        """
        if not any((isinstance(tolerance, int), isinstance(edge_tolerance, int))):
            raise ValueError(f"Width and height are not int {type(tolerance), type(edge_tolerance)}")
        return tolerance, edge_tolerance
