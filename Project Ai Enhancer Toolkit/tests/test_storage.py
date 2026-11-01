
from pathlib import Path

import numpy as np
import pytest

from database import database
import save
import main


@pytest.fixture
def temporary_database(tmp_path, monkeypatch):
    """Give each test its own temporary database."""

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        tmp_path / "gallery.db"
    )

    database.initialize_database()

    return tmp_path


def test_database_registration(temporary_database):
    """Check that a registered image can become gallery-ready."""

    image_path = temporary_database / "image.jpg"
    image_path.write_bytes(b"test image")

    image_id = database.add_image(
        output_name="image.jpg",
        output_path=str(image_path),
        operation="Resize",
        width=800,
        height=600
    )

    database.update_image_status(image_id, "ready")

    images = database.get_images()

    assert len(images) == 1
    assert images[0]["id"] == image_id
    assert images[0]["output_name"] == "image.jpg"


def test_synchronize_missing_images(temporary_database):
    """Check that missing image files lose their database records."""

    image_path = temporary_database / "missing.jpg"

    image_id = database.add_image(
        output_name="missing.jpg",
        output_path=str(image_path),
        operation="Resize",
        width=800,
        height=600
    )

    database.update_image_status(image_id, "ready")

    database.synchronize_images()

    assert database.get_image(image_id) is None


def test_expired_image_detection(temporary_database):
    """Check that images older than 30 days become deleting."""

    image_path = temporary_database / "old.jpg"
    image_path.write_bytes(b"old image")

    image_id = database.add_image(
        output_name="old.jpg",
        output_path=str(image_path),
        operation="Resize",
        width=800,
        height=600
    )

    database.update_image_status(image_id, "ready")

    # Give the record an artificially old timestamp.
    with database.get_connection() as connection:
        connection.execute("""
            UPDATE images
            SET created_at = '2000-01-01T00:00:00'
            WHERE id = ?
        """, (image_id,))

    expired = database.mark_expired_images()

    assert any(item[0] == image_id for item in expired)
    assert database.get_image(image_id)["status"] == "deleting"


def test_staging_and_publishing(temporary_database, monkeypatch):
    """Check that staged images can be published."""

    monkeypatch.setattr(
        save,
        "OUTPUT_DIR",
        temporary_database / "saved_images"
    )

    monkeypatch.setattr(
        save,
        "STAGING_DIR",
        temporary_database / ".staging_images"
    )

    image = np.zeros((20, 20, 3), dtype=np.uint8)

    staged_path = save.create_staged_image(image)
    final_path = save.get_final_path(staged_path)

    assert Path(staged_path).is_file()

    save.publish_staged_image(
        staged_path,
        final_path
    )

    assert Path(final_path).is_file()
    assert not Path(staged_path).exists()


def test_recover_pending_image(temporary_database, monkeypatch):
    """Check that an interrupted save can be recovered."""

    output_dir = temporary_database / "saved_images"
    staging_dir = temporary_database / ".staging_images"

    monkeypatch.setattr(save, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(save, "STAGING_DIR", staging_dir)

    monkeypatch.setattr(main, "OUTPUT_DIR", output_dir)
    monkeypatch.setattr(main, "STAGING_DIR", staging_dir)

    image = np.zeros((20, 20, 3), dtype=np.uint8)

    staged_path = save.create_staged_image(image)
    final_path = save.get_final_path(staged_path)

    image_id = database.add_image(
        output_name=Path(final_path).name,
        output_path=str(final_path),
        staging_path=staged_path,
        operation="Resize",
        width=20,
        height=20
    )

    # Simulate an interrupted application before publishing.
    main.recover_pending_images()

    record = database.get_image(image_id)

    assert Path(final_path).is_file()
    assert record["status"] == "ready"
    assert record["staging_path"] is None


def test_gallery_image_deletion(temporary_database):
    """Check that deleting an image removes both file and record."""

    image_path = temporary_database / "image.jpg"
    image_path.write_bytes(b"test image")

    image_id = database.add_image(
        output_name="image.jpg",
        output_path=str(image_path),
        operation="Resize",
        width=800,
        height=600
    )

    database.update_image_status(image_id, "ready")

    main.delete_image(image_id)

    assert not image_path.exists()
    assert database.get_image(image_id) is None


def test_image_download(temporary_database):
    """Check that an image can be copied to a download destination."""

    image_path = temporary_database / "image.jpg"
    download_path = temporary_database / "downloads" / "image.jpg"

    image_path.write_bytes(b"test image")

    image_id = database.add_image(
        output_name="image.jpg",
        output_path=str(image_path),
        operation="Resize",
        width=800,
        height=600
    )

    database.update_image_status(image_id, "ready")

    result = main.download_image(
        image_id,
        download_path
    )

    assert Path(result).is_file()
    assert download_path.read_bytes() == image_path.read_bytes()
    assert image_path.exists()
