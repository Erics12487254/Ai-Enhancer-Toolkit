
from pathlib import Path
from uuid import uuid4
import shutil

import cv2


class ImageStorage:
    def __init__(self):
        """Initialize image storage directories."""

        self.base_dir = Path(__file__).resolve().parent

        # Permanent image storage.
        self.output_dir = self.base_dir / "saved_images"

        # Temporary storage for images awaiting database registration.
        self.staging_dir = self.base_dir / ".staging_images"

    def create_staged_image(self, result):
        """Write a processed image to temporary storage."""

        self.staging_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{uuid4().hex}.jpg"
        staged_path = self.staging_dir / filename

        if not cv2.imwrite(str(staged_path), result):
            raise OSError(
                f"Could not write temporary image: {staged_path}"
            )

        return str(staged_path.resolve())

    def get_final_path(self, staged_path):
        """Determine the permanent destination of a staged image."""

        staged_path = Path(staged_path)

        return self.output_dir / staged_path.name

    def publish_staged_image(self, staged_path, output_path):
        """Move a staged image into permanent storage."""

        staged_path = Path(staged_path)
        output_path = Path(output_path)

        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not staged_path.is_file():
            raise FileNotFoundError(
                f"Staged image does not exist: {staged_path}"
            )

        if output_path.exists():
            raise FileExistsError(
                f"Output image already exists: {output_path}"
            )

        staged_path.replace(output_path)

        return str(output_path.resolve())

    def delete_image_file(self, image_path):
        """Delete an image file if it exists."""

        image_path = Path(image_path)
        image_path.unlink(missing_ok=True)

    def copy_image(self, source_path, destination_path):
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

    def save_image(self, result, output_path=None, source_path=None):
        """
        Standalone image-saving function.

        The main application uses the staging workflow instead.
        """

        self.output_dir.mkdir(parents=True, exist_ok=True)

        if output_path is None:
            output_path = self.output_dir / f"{uuid4().hex}.jpg"
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
