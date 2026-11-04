import cv2


def load_image(path):
    """Load an image in OpenCV's default color format."""

    image = cv2.imread(str(path), cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError(f"Could not load image: {path}")

    return image