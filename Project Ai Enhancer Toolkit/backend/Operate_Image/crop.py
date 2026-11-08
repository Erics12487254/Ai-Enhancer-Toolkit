import numpy as np


def crop_image(image, x=100, y=100, width=400, height=400):
    """Return a rectangular crop from an image."""

    if not isinstance(image, np.ndarray):
        raise TypeError("Input must be a NumPy array.")

    if not all(isinstance(value, int) for value in (x, y, width, height)):
        raise ValueError("Crop coordinates and dimensions must be integers.")

    if x < 0 or y < 0 or width <= 0 or height <= 0:
        raise ValueError(
            "Crop coordinates must be nonnegative and dimensions positive."
        )

    image_height, image_width = image.shape[:2]

    if x + width > image_width or y + height > image_height:
        raise ValueError("The crop area extends beyond the image bounds.")

    return image[y:y + height, x:x + width]