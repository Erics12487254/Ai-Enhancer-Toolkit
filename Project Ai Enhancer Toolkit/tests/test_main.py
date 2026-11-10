
import sys
from pathlib import Path

import numpy as np
import pytest


# Make the application source directory importable during testing.
APP_SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_SOURCE))

import main


class FakeStorage:
    """Replace real image storage during application tests."""

    def __init__(self):
        self.output_dir = Path("test-gallery")
        self.saved_image = None
        self.saved_format = None
        self.download_request = None
        self.deleted_path = None

    def save_image(self, image, output_format="jpg"):
        self.saved_image = image
        self.saved_format = output_format
        return "saved-image.jpg"

    def copy_image(self, image_path, destination_path):
        self.download_request = (image_path, destination_path)
        return str(destination_path)

    def delete_image(self, image_path):
        self.deleted_path = image_path


@pytest.fixture
def storage():
    return FakeStorage()


@pytest.fixture
def application(storage):
    return main.Application(storage)


# --------------------------------------------------
# Image validation
# --------------------------------------------------

def test_validate_input_accepts_valid_image(
    application,
    monkeypatch,
):
    monkeypatch.setattr(
        main,
        "load_image",
        lambda path: np.zeros((10, 10, 3), dtype=np.uint8),
    )

    result = application.validate_input("source.jpg")

    assert result == "source.jpg"


def test_validate_input_rejects_empty_path(application):
    with pytest.raises(ValueError):
        application.validate_input("")


# --------------------------------------------------
# Image processing
# --------------------------------------------------

def test_process_image_uses_requested_operation(
    application,
    storage,
    monkeypatch,
):
    source_image = np.zeros((10, 10, 3), dtype=np.uint8)
    enhanced_image = np.ones((20, 20, 3), dtype=np.uint8)

    monkeypatch.setattr(
        main,
        "load_image",
        lambda path: source_image,
    )

    # Replace the real enhancement function with a predictable test function.
    monkeypatch.setitem(
        main.OPERATIONS,
        "Enhance the image ✦",
        lambda image: enhanced_image,
    )

    result = application.process_image(
        path="source.jpg",
        operation="Enhance the image ✦",
        output_format="png",
    )

    assert result == "saved-image.jpg"
    assert storage.saved_image is enhanced_image
    assert storage.saved_format == "png"


def test_process_image_rejects_non_dictionary_settings(
    application,
    monkeypatch,
):
    monkeypatch.setattr(
        main,
        "load_image",
        lambda path: np.zeros((10, 10, 3), dtype=np.uint8),
    )

    with pytest.raises(
        ValueError,
        match="Operation settings must be a dictionary",
    ):
        application.process_image(
            path="source.jpg",
            operation="Enhance the image ✦",
            settings=["invalid"],
        )


def test_process_image_rejects_unknown_operation(
    application,
    monkeypatch,
):
    monkeypatch.setattr(
        main,
        "load_image",
        lambda path: np.zeros((10, 10, 3), dtype=np.uint8),
    )

    with pytest.raises(
        ValueError,
        match="Choose a valid operation",
    ):
        application.process_image(
            path="source.jpg",
            operation="Rotate the image",
        )


def test_process_image_rejects_unimplemented_operation(
    application,
    monkeypatch,
):
    monkeypatch.setitem(
        main.OPERATIONS,
        "Resize the image",
        lambda image: None,
    )

    monkeypatch.setattr(
        main,
        "load_image",
        lambda path: np.zeros((10, 10, 3), dtype=np.uint8),
    )

    with pytest.raises(ValueError):
        application.process_image(
            path="source.jpg",
            operation="Resize the image",
        )


# --------------------------------------------------
# Enhancement preparation
# --------------------------------------------------

def test_prepare_enhancement_delegates_to_backend(
    application,
    monkeypatch,
):
    preparation_called = []

    monkeypatch.setattr(
        main,
        "prepare_enhancement_engine",
        lambda: preparation_called.append(True),
    )

    application.prepare_enhancement()

    assert preparation_called == [True]


# --------------------------------------------------
# Gallery
# --------------------------------------------------

def test_gallery_images_include_preview_data(
    application,
    monkeypatch,
):
    monkeypatch.setattr(
        main,
        "list_gallery_images",
        lambda output_dir: [
            {
                "path": "saved-image.jpg",
                "filename": "saved-image.jpg",
            }
        ],
    )

    monkeypatch.setattr(
        main,
        "make_thumbnail_data",
        lambda path: {
            "thumbnail_data": "encoded-thumbnail",
            "width": 120,
            "height": 80,
        },
    )

    images = application.get_gallery_images()

    assert images == [
        {
            "path": "saved-image.jpg",
            "filename": "saved-image.jpg",
            "thumbnail_data": "encoded-thumbnail",
            "width": 120,
            "height": 80,
        }
    ]


# --------------------------------------------------
# Download and deletion
# --------------------------------------------------

def test_download_image_is_forwarded_to_storage(
    application,
    storage,
):
    application.download_image(
        "saved.jpg",
        "download.jpg",
    )

    assert storage.download_request == (
        "saved.jpg",
        "download.jpg",
    )


def test_delete_image_is_forwarded_to_storage(
    application,
    storage,
):
    application.delete_image("saved.jpg")

    assert storage.deleted_path == "saved.jpg"
