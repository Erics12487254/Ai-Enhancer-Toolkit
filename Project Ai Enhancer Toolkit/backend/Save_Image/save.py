from pathlib import Path
import shutil
from uuid import uuid4

import cv2


class ImageStorage:
    """Save, copy, and delete processed image files."""

    SUPPORTED_FORMATS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp",
    }

    def __init__(self, output_dir=None):
        self.output_dir = (
            Path(output_dir)
            if output_dir is not None
            else Path(__file__).resolve().parent / "saved_images"
        )

    def save_image(self, image, output_format="jpg"):
        """Save an image using a supported format."""

        if image is None or not hasattr(image, "size") or image.size == 0:
            raise ValueError("Cannot save an empty image.")

        extension = f".{str(output_format).lstrip('.').lower()}"

        if extension not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported output format: {output_format}")

        self.output_dir.mkdir(parents=True, exist_ok=True)
        output_path = self.output_dir / f"{uuid4().hex}{extension}"

        try:
            success = cv2.imwrite(str(output_path), image)
            if not success:
                raise OSError(f"Could not save image: {output_path}")
        except Exception:
            output_path.unlink(missing_ok=True)
            raise

        return str(output_path.resolve())

    def copy_image(self, source_path, destination_path):
        """Copy a stored image to another location."""

        source_path = self._validate_managed_path(source_path)
        destination_path = Path(destination_path).resolve()

        if not source_path.is_file():
            raise FileNotFoundError(f"Image does not exist: {source_path}")

        if source_path == destination_path:
            raise ValueError(
                "The download destination cannot be the original image."
            )

        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination_path)
        return str(destination_path)

    def delete_image(self, image_path):
        """Delete an image from the managed storage directory."""

        image_path = self._validate_managed_path(image_path)
        image_path.unlink(missing_ok=True)

    def _validate_managed_path(self, image_path):
        """Reject paths outside the managed storage directory."""

        image_path = Path(image_path).resolve()
        output_dir = self.output_dir.resolve()

        try:
            image_path.relative_to(output_dir)
        except ValueError:
            raise ValueError(
                "The image is outside the storage directory."
            ) from None

        return image_path