import cv2

# Application workflow: validate input, run the requested operation, then save its result.
from enhance import enhance_image
from loader import load_image
from resize import resize_image
from save import save_image


OPERATIONS = {
    "Resize the image": resize_image,
    "Enhance the image": enhance_image,
}


def validate_input(path):
    """Check that OpenCV can decode the selected image."""
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Select an image first.")

    load_image(str(path))
    return path


def process_image(path, operation, output_path=None):
    """Run one supported operation and save the result; return its location."""
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Select an image first.")

    try:
        operation_function = OPERATIONS[operation]
    except (KeyError, TypeError):
        raise ValueError("Choose a valid operation.") from None

    image = load_image(str(path))
    try:
        result = operation_function(image)
    except cv2.error as error:
        raise ValueError(f"Could not process the image: {error}") from error

    if result is None:
        raise ValueError(f"{operation} is not implemented yet.")

    try:
        return save_image(result, output_path=output_path, source_path=path)
    except cv2.error as error:
        raise ValueError(f"Could not save the processed image: {error}") from error
