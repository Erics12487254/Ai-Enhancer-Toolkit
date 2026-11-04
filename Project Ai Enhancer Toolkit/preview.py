import base64

import cv2

from loader import load_image


def make_thumbnail_data(image_path, max_width=140, max_height=100):
    """Return preview fields for an image, or empty preview fields."""

    try:
        image = load_image(image_path)
    except (OSError, ValueError, cv2.error):
        return {
            "thumbnail_data": None,
            "width": None,
            "height": None,
        }

    height, width = image.shape[:2]
    scale = min(max_width / width, max_height / height)

    thumbnail = cv2.resize(
        image,
        (
            max(1, int(width * scale)),
            max(1, int(height * scale)),
        ),
    )

    success, encoded = cv2.imencode(".png", thumbnail)

    if not success:
        thumbnail_data = None
    else:
        thumbnail_data = base64.b64encode(encoded).decode("ascii")

    return {
        "thumbnail_data": thumbnail_data,
        "width": width,
        "height": height,
    }