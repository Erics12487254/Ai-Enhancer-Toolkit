from pathlib import Path

from save import ImageStorage


def list_gallery_images(output_dir=None):
    """Return basic records for supported images in the gallery."""

    if output_dir is None:
        output_dir = ImageStorage().output_dir

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    records = []

    for image_path in output_dir.iterdir():
        if not image_path.is_file():
            continue

        if image_path.suffix.lower() not in ImageStorage.SUPPORTED_FORMATS:
            continue

        records.append({
            "path": str(image_path.resolve()),
            "filename": image_path.name,
            "created_at": image_path.stat().st_mtime,
        })

    return sorted(
        records,
        key=lambda record: record["created_at"],
        reverse=True,
    )