from pathlib import Path

import cv2


def save_image(result, output_path=None, source_path=None):
    """Save an image and return its path, raising an error if writing fails."""
    if output_path is None:
        output_path = Path.cwd() / "saved_image.jpg"
    else:
        output_path = Path(output_path)

    # Avoid overwriting the source if it happens to use the default output name.
    if source_path is not None and output_path.resolve() == Path(source_path).resolve():
        output_path = output_path.with_name(f"{output_path.stem}_processed{output_path.suffix}")

    if not cv2.imwrite(str(output_path), result):
        raise OSError(f"Could not save the processed image to: {output_path}")

    return str(output_path)
