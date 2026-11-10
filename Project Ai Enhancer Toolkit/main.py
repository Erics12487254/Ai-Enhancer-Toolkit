
import cv2

from backend.Load_Image.loader import load_image

from backend.Operate_Image.blur import blur_image  # Future development
from backend.Operate_Image.crop import crop_image  # Future development
from backend.Operate_Image.sharpen import sharpen_image  # Future development
from backend.Operate_Image.resize import resize_image  # Future development

from backend.Operate_Image.enhance import (
    enhance_image,
    prepare_enhancement as prepare_enhancement_engine,
)

from backend.Save_Image.save import ImageStorage
from backend.Save_Image.gallery import list_gallery_images
from backend.Save_Image.preview import make_thumbnail_data


OPERATIONS = {
    "Resize the image": resize_image,  # Future development
    "Crop the image": crop_image,  # Future development
    "Blur the image": blur_image,  # Future development
    "Sharpen the image": sharpen_image,  # Future development
    "Enhance the image ✦": enhance_image,
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
        """Check that the path points to a readable image."""

        if not isinstance(path, (str, bytes)) or not str(path).strip():
            raise ValueError("Select an image first.")

        try:
            load_image(path)
        except (OSError, ValueError, cv2.error) as error:
            raise ValueError(f"Could not load image: {error}") from error

        return path

    def prepare_enhancement(self):
        """Prepare the Real-ESRGAN engine before image inference."""

        # Delegate engine initialization to the enhancement backend.
        prepare_enhancement_engine()

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

        try:
            image = load_image(path)
            result = operation_function(image, **settings)

        except (OSError, ValueError, TypeError, cv2.error) as error:
            raise ValueError(
                f"Could not process the image: {error}"
            ) from error

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

        self.storage.delete_image(image_path)
