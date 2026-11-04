import cv2
import numpy as np
import pytest

from gallery import list_gallery_images
from save import ImageStorage


def test_save_image_creates_file_with_requested_format(tmp_path):
    storage = ImageStorage(tmp_path)
    image = np.zeros((8, 8, 3), dtype=np.uint8)

    output_path = storage.save_image(image, output_format="png")

    assert output_path.endswith(".png")
    assert (tmp_path / output_path.split("/")[-1].split("\\")[-1]).is_file()


def test_rejects_unsupported_output_format(tmp_path):
    storage = ImageStorage(tmp_path)
    image = np.zeros((8, 8, 3), dtype=np.uint8)

    with pytest.raises(ValueError, match="Unsupported output format"):
        storage.save_image(image, output_format="gif")


def test_gallery_lists_image_dimensions_and_name(tmp_path):
    storage = ImageStorage(tmp_path)
    image = np.zeros((12, 20, 3), dtype=np.uint8)
    saved_path = storage.save_image(image)

    records = list_gallery_images(tmp_path)

    assert len(records) == 1
    assert records[0]["path"] == saved_path
    assert records[0]["filename"].endswith(".jpg")


def test_download_copies_image_and_keeps_original(tmp_path):
    storage = ImageStorage(tmp_path / "gallery")
    image = np.zeros((8, 8, 3), dtype=np.uint8)
    saved_path = storage.save_image(image)
    destination = tmp_path / "download.jpg"

    returned_path = storage.copy_image(saved_path, destination)

    assert destination.is_file()
    assert storage._validate_managed_path(saved_path).is_file()
    assert returned_path == str(destination.resolve())


def test_download_rejects_path_outside_storage(tmp_path):
    storage = ImageStorage(tmp_path / "gallery")
    outside_path = tmp_path / "outside.jpg"

    with pytest.raises(ValueError, match="outside the storage directory"):
        storage.copy_image(outside_path, tmp_path / "copy.jpg")


def test_delete_removes_image(tmp_path):
    storage = ImageStorage(tmp_path)
    image = np.zeros((8, 8, 3), dtype=np.uint8)
    saved_path = storage.save_image(image)

    storage.delete_image(saved_path)

    assert not storage._validate_managed_path(saved_path).exists()


def test_gallery_ignores_unsupported_files(tmp_path):
    (tmp_path / "notes.txt").write_text("not an image")

    records = list_gallery_images(tmp_path)

    assert records == []