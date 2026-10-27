import cv2

# Application workflow: validate input, run the requested operation, then save its result.
from enhance import enhance_image
from loader import load_image
from resize import resize_image
from save import save_image
from crop import crop_image
from blur import blur_image
from sharpen import sharpen_image


OPERATIONS = {
    "Resize the image": resize_image,
    "Enhance the image": enhance_image,
    "Crop the image": crop_image,
    "Blur the image": blur_image,
    "Sharpen the image": sharpen_image
}

def _validate_path(path):
    if not isinstance(path, str) or not path.strip():
        raise ValueError("Select an image first.")


def validate_input(path):
    """Check that OpenCV can decode the selected image."""
    _validate_path(path)
    load_image(path)
    return path

# Validate the path even if the caller skipped validate_input().
def process_image(path, operation, output_path=None): 
    """Run one supported operation and save the result; return its location."""
    _validate_path(path)

    try:
        operation_function = OPERATIONS[operation]
    except (KeyError, TypeError):
        raise ValueError("Choose a valid operation.") from None

    image = load_image((path))
    try:
        result = operation_function(image)
    except cv2.error as error:
        raise ValueError(f"Could not process the image: {error}") from error

    #will be remove later
    if result is None:
        raise ValueError(f"{operation} is not implemented yet.")

    try:
        return save_image(result, output_path=output_path, source_path=path)#source_path=protect from being overwritten, Output path: where to write the processed result.
    except cv2.error as error:
        raise ValueError(f"Could not save the processed image: {error}") from error
