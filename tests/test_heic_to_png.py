import os
from pathlib import Path

import pytest
from src.logo_bg_vanisher import AspectRatioSizer
from src.logo_bg_vanisher.folder_utils import load_image
from src.logo_bg_vanisher import SavePic

TEST_FOLDER = Path(__file__).parents[0]


@pytest.fixture
def heic_file() -> Path:
    return TEST_FOLDER / "heic/electrical_outlet.HEIC"


@pytest.fixture
def expected_heic_resize() -> Path:
    return TEST_FOLDER / "heic/electrical_outlet.png"


def test_heic_autoscaler_resize(heic_file, expected_heic_resize):
    image_object = load_image(picture=heic_file)

    image_saver = SavePic(img=image_object)
    image_saver.save_image()

    # Check if processed image was created
    assert expected_heic_resize.exists(), "Processed image file does not exist"

    # Clean up
    os.remove(expected_heic_resize)
