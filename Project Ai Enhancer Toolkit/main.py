import cv2

from blur import blur_image
from crop import crop_image
from enhance import enhance_image
from gallery import list_gallery_images
from loader import load_image
from preview import make_thumbnail_data
from resize import resize_image
from save import ImageStorage
from sharpen import sharpen_image


OPERATIONS = {
    "Resize the image": resize_image,
    "Enhance the image": enhance_image,
    "Crop the image": crop_image,
    "Blur the image": blur_image,
    "Sharpen the image": sharpen_image,
}

OPERATION_SETTINGS = {
    "Resize the image": {"width", "height"},
    "Enhance the image": set(),
    "Crop the image": {"x", "y", "width", "height"},
    "Blur the image": set(),
    "Sharpen the image": set(),
}


def create_application(storage=None):
    """Create an application and its storage dependency."""

    if storage is None:
        storage = ImageStorage()

    return Application(storage)


class Application:
    """Coordinate frontend requests and backend modules."""

    def __init__(self, storage):
        self.storage = storage

    def validate_input(self, path):
        """Check that the path points to an image the loader can read."""

        if not isinstance(path, (str, bytes)) or not str(path).strip():
            raise ValueError("Select an image first.")

        try:
            load_image(path)
        except (OSError, cv2.error) as error:
            raise ValueError(f"Could not load image: {error}") from error

        return path

    def process_image(
        self,
        path,
        operation,
        settings=None,
        output_format="jpg",
    ):
        """Load, process, and save an image."""

        self.validate_input(path)

        try:
            operation_function = OPERATIONS[operation]
        except (KeyError, TypeError):
            raise ValueError("Choose a valid operation.") from None

        settings = {} if settings is None else settings

        if not isinstance(settings, dict):
            raise ValueError("Operation settings must be a dictionary.")

        allowed_settings = OPERATION_SETTINGS[operation]
        unknown_settings = set(settings) - allowed_settings

        if unknown_settings:
            names = ", ".join(sorted(unknown_settings))
            raise ValueError(
                f"Unsupported settings for {operation}: {names}"
            )

        try:
            image = load_image(path)
            result = operation_function(image, **settings)
        except (OSError, cv2.error) as error:
            raise ValueError(f"Could not process the image: {error}") from error

        if result is None:
            raise ValueError(f"{operation} is not implemented yet.")

        if not hasattr(result, "shape") or result.size == 0:
            raise ValueError(
                "The processing operation returned an invalid image."
            )

        return self.storage.save_image(
            result,
            output_format=output_format,
        )

    def get_gallery_images(self):
        """Return gallery records and preview data for the frontend."""

        images = list_gallery_images(self.storage.output_dir)

        for record in images:
            preview = make_thumbnail_data(record["path"])
            record.update(preview)

        return images

    def download_image(self, image_path, destination_path):
        """Copy a gallery image to a chosen destination."""

        return self.storage.copy_image(image_path, destination_path)

    def delete_image(self, image_path):
        """Delete a gallery image."""

        return self.storage.delete_image(image_path)