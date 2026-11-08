import sys
from pathlib import Path

import numpy as np
import pytest


APP_SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_SOURCE))

import main


class FakeStorage:
    """Minimal storage replacement for application-layer tests."""

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


def test_process_image_uses_the_requested_operation(monkeypatch):
    storage = FakeStorage()
    application = main.Application(storage)

    source_image = np.zeros((10, 10, 3), dtype=np.uint8)
    processed_image = np.ones((5, 8, 3), dtype=np.uint8)

    monkeypatch.setattr(main, "load_image", lambda path: source_image)
    monkeypatch.setitem(
        main.OPERATIONS,
        "Resize the image",
        lambda image, width, height: processed_image,
    )

    result = application.process_image(
        path="source.jpg",
        operation="Resize the image",
        settings={"width": 8, "height": 5},
        output_format="png",
    )

    assert result == "saved-image.jpg"
    assert storage.saved_image is processed_image
    assert storage.saved_format == "png"


def test_process_image_rejects_non_dictionary_settings():
    application = main.Application(FakeStorage())

    with pytest.raises(
        ValueError,
        match="Operation settings must be a dictionary",
    ):
        application.process_image(
            path="source.jpg",
            operation="Blur the image",
            settings=["invalid"],
        )


def test_process_image_rejects_unknown_operation():
    application = main.Application(FakeStorage())

    with pytest.raises(ValueError, match="Choose a valid operation"):
        application.process_image(
            path="source.jpg",
            operation="Rotate the image",
        )


def test_gallery_images_include_preview_data(monkeypatch):
    storage = FakeStorage()
    application = main.Application(storage)

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


def test_download_and_delete_are_forwarded_to_storage():
    storage = FakeStorage()
    application = main.Application(storage)

    application.download_image("saved.jpg", "download.jpg")
    application.delete_image("saved.jpg")

    assert storage.download_request == ("saved.jpg", "download.jpg")
    assert storage.deleted_path == "saved.jpg"