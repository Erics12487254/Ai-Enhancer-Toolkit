import cv2

Default_width, Default_height = 800, 600
Min_width, Min_height = 100, 100
Max_width, Max_height = 7680, 4320

def resize_image(image, width=Default_width, height=Default_height):
    """Resize an image to the requested dimensions."""

    if not isinstance(width, int) or not isinstance(height, int):
        raise ValueError("Width and height must be integers.")

    if not Min_width <= width <= Max_width:
        raise ValueError(
            f"Width must be between {Min_width} and {Max_width}."
        )

    if not Min_height <= height <= Max_height:
        raise ValueError(
            f"Height must be between {Min_height} and {Max_height}."
        )

    return cv2.resize(image, (width, height))