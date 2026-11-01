
from pathlib import Path
from uuid import uuid4
import shutil

import cv2


BASE_DIR = Path(__file__).resolve().parent

# Permanent image storage.
OUTPUT_DIR = BASE_DIR / "saved_images"

# Temporary storage for images awaiting database registration.
STAGING_DIR = BASE_DIR / ".staging_images"


def create_staged_image(result):
    """Write a processed image to temporary storage."""

    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid4().hex}.jpg"
    staged_path = STAGING_DIR / filename

    if not cv2.imwrite(str(staged_path), result):
        raise OSError(
            f"Could not write temporary image: {staged_path}"
        )

    return str(staged_path.resolve())


def get_final_path(staged_path):
    """Determine the permanent destination of a staged image."""

    staged_path = Path(staged_path)

    return OUTPUT_DIR / staged_path.name


def publish_staged_image(staged_path, output_path):
    """Move a staged image into permanent storage."""

    staged_path = Path(staged_path)
    output_path = Path(output_path)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not staged_path.is_file():
        raise FileNotFoundError(
            f"Staged image does not exist: {staged_path}"
        )

    if output_path.exists():
        raise FileExistsError(
            f"Output image already exists: {output_path}"
        )

    # Both directories are inside the project folder.
    # Path.replace moves the file to its permanent location.
    staged_path.replace(output_path)

    return str(output_path.resolve())


def delete_image_file(image_path):
    """Delete an image file if it exists."""

    image_path = Path(image_path)
    image_path.unlink(missing_ok=True)


def copy_image(source_path, destination_path):
    """Copy a saved image to a user-selected download location."""

    source_path = Path(source_path)
    destination_path = Path(destination_path)

    if not source_path.is_file():
        raise FileNotFoundError(
            f"Image does not exist: {source_path}"
        )

    if source_path.resolve() == destination_path.resolve():
        raise ValueError(
            "The download destination cannot be the original image."
        )

    destination_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copy2(source_path, destination_path)

    return str(destination_path.resolve())


def save_image(result, output_path=None, source_path=None):
    """
    Standalone image-saving function.

    The main application uses the staging workflow instead.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if output_path is None:
        output_path = OUTPUT_DIR / f"{uuid4().hex}.jpg"
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    if source_path is not None:
        if output_path.resolve() == Path(source_path).resolve():
            output_path = output_path.with_name(
                f"{output_path.stem}_{uuid4().hex}{output_path.suffix}"
            )

    if output_path.exists():
        raise FileExistsError(
            f"Output image already exists: {output_path}"
        )

    if not cv2.imwrite(str(output_path), result):
        raise OSError(
            f"Could not save image: {output_path}"
        )

    return str(output_path.resolve())
