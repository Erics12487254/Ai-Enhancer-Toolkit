import cv2


def resize_image(image, width=800, height=600):
    """Resize an image to the requested dimensions."""

    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError("Width and height must be integers.")

    if width <= 0 or height <= 0:
        raise ValueError("Width and height must be positive.")

    return cv2.resize(image, (width, height))