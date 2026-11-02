
# Standard dependencies
import cv2
import sqlite3
from pathlib import Path

# Image processing operations
from enhance import enhance_image
from loader import load_image
from resize import resize_image
from crop import crop_image
from blur import blur_image
from sharpen import sharpen_image

# Image storage service
from save import ImageStorage

# Database service
from database.database import ImageDatabase


# Initialize independent services
image_storage = ImageStorage()
image_database = ImageDatabase()


OPERATIONS = {
    "Resize the image": resize_image,
    "Enhance the image": enhance_image,
    "Crop the image": crop_image,
    "Blur the image": blur_image,
    "Sharpen the image": sharpen_image
}


class ApplicationError(Exception):
    """A user-facing error raised by the application layer."""


def _database_call(function, *args, **kwargs):
    """Run a database operation without exposing SQLite errors to the GUI."""

    try:
        return function(*args, **kwargs)

    except sqlite3.Error as error:
        raise ApplicationError(
            f"A database operation failed: {error}"
        ) from error


def _validate_path(path):
    """Ensure that an image path is provided."""

    if not isinstance(path, str) or not path.strip():
        raise ValueError("Select an image first.")


def validate_input(path):
    """Check that OpenCV can decode the selected image."""

    _validate_path(path)
    load_image(path)

    return path


def process_image(path, operation, output_path=None):
    """
    Process an image, stage it, register it,
    and publish it to permanent storage.
    """

    _validate_path(path)

    try:
        operation_function = OPERATIONS[operation]

    except (KeyError, TypeError):
        raise ValueError("Choose a valid operation.") from None

    image = load_image(path)

    try:
        result = operation_function(image)

    except cv2.error as error:
        raise ValueError(
            f"Could not process the image: {error}"
        ) from error

    if result is None:
        raise ValueError(
            f"{operation} is not implemented yet."
        )

    if output_path is not None:
        raise ValueError(
            "Custom output paths are not supported by the gallery workflow yet."
        )

    # Step 1: Write the processed image to temporary storage.
    staged_path = image_storage.create_staged_image(result)

    # Step 2: Determine its permanent destination.
    final_path = image_storage.get_final_path(staged_path)

    # Step 3: Register the image as pending.
    try:
        image_id = _database_call(
            image_database.add_image,
            output_name=final_path.name,
            output_path=str(final_path.resolve()),
            staging_path=staged_path,
            operation=operation,
            width=result.shape[1],
            height=result.shape[0]
        )

    except Exception:
        # If registration fails, remove the unregistered staged file.
        image_storage.delete_image_file(staged_path)
        raise

    # Step 4: Move the staged image into permanent storage.
    # If this fails, the pending record remains for recovery.
    try:
        image_storage.publish_staged_image(
            staged_path,
            final_path
        )

        # Step 5: Make the image visible to the gallery.
        _database_call(
            image_database.update_image_status,
            image_id,
            "ready"
        )

    except (OSError, ApplicationError) as error:
        raise RuntimeError(
            "The image was registered but could not be fully published. "
            "The application will attempt recovery on its next maintenance run."
        ) from error

    return str(final_path.resolve())


def recover_pending_images():
    """
    Recover interrupted saves.

    If the final file exists, mark it ready.
    Otherwise, try to publish the staged file.
    """

    pending_images = _database_call(
        image_database.get_pending_images
    )

    for record in pending_images:

        image_id = record["id"]
        final_path = Path(record["output_path"])
        staged_path = (
            Path(record["staging_path"])
            if record["staging_path"]
            else None
        )

        try:
            if final_path.is_file():

                # The move succeeded, but the database update may have failed.
                _database_call(
                    image_database.update_image_status,
                    image_id,
                    "ready"
                )

                if staged_path and staged_path.exists():
                    image_storage.delete_image_file(staged_path)

            elif staged_path and staged_path.is_file():

                # The application stopped before publishing the image.
                image_storage.publish_staged_image(
                    staged_path,
                    final_path
                )

                _database_call(
                    image_database.update_image_status,
                    image_id,
                    "ready"
                )

            else:

                # Neither file exists, so remove the unusable record.
                _database_call(
                    image_database.delete_image_record,
                    image_id
                )

        except (OSError, ApplicationError) as error:
            print(
                f"Could not recover image {image_id}: {error}"
            )


def cleanup_orphan_staging_files():
    """
    Remove staged files that have no pending database record.
    """

    image_storage.staging_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    pending_images = _database_call(
        image_database.get_pending_images
    )

    known_staging_paths = {
        Path(record["staging_path"]).resolve()
        for record in pending_images
        if record["staging_path"]
    }

    for staged_file in image_storage.staging_dir.iterdir():

        if staged_file.is_file():
            if staged_file.resolve() not in known_staging_paths:

                try:
                    image_storage.delete_image_file(staged_file)

                except OSError as error:
                    print(
                        f"Could not remove temporary file "
                        f"{staged_file}: {error}"
                    )


def cleanup_expired_images():
    """Delete expired image files and their database records."""

    expired_images = _database_call(
        image_database.mark_expired_images
    )

    for image_id, output_path in expired_images:

        try:
            # Remove the actual image file first.
            image_storage.delete_image_file(output_path)

            # Only then remove its database record.
            _database_call(
                image_database.delete_image_record,
                image_id
            )

        except (OSError, ApplicationError) as error:
            # The deleting record remains for another attempt.
            print(
                f"Could not delete expired image "
                f"{output_path}: {error}"
            )


def delete_image(image_id):
    """Delete one gallery image and its database record."""

    record = _database_call(
        image_database.get_image,
        image_id
    )

    if record is None:
        raise ValueError("Image record was not found.")

    # Hide it from the gallery before attempting deletion.
    _database_call(
        image_database.update_image_status,
        image_id,
        "deleting"
    )

    # If file deletion fails, the deleting record remains for retry.
    image_storage.delete_image_file(record["output_path"])

    _database_call(
        image_database.delete_image_record,
        image_id
    )


def download_image(image_id, destination_path):
    """Copy one gallery image to the user's chosen location."""

    record = _database_call(
        image_database.get_image,
        image_id
    )

    if record is None or record["status"] != "ready":
        raise ValueError("Image is not available for download.")

    return image_storage.copy_image(
        record["output_path"],
        destination_path
    )


def run_maintenance():
    """Run storage recovery, synchronization, and expiration cleanup."""

    recover_pending_images()

    _database_call(
        image_database.synchronize_images
    )

    cleanup_expired_images()
    cleanup_orphan_staging_files()


def initialize_app():
    """Initialize the database and perform startup maintenance."""

    _database_call(
        image_database.initialize_database
    )

    run_maintenance()


def get_gallery_images():
    """Return the images currently available to the gallery."""

    return _database_call(
        image_database.get_images
    )
