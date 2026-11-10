
import sys
from pathlib import Path

import cv2
import numpy as np

APP_SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_SOURCE))

import main


class FakeStorage:
    """Capture application save requests without writing real files."""

    def __init__(self, events):
        self.output_dir = Path("test-gallery")
        self.saved_image = None
        self.saved_format = None
        self.events = events

    def save_image(self, image, output_format="jpg"):
        self.events.append("save")

        self.saved_image = image
        self.saved_format = output_format

        return "test-gallery/result.png"


def test_complete_image_processing_workflow(
    tmp_path,
    monkeypatch,
):
    events = []

    # Create a real temporary input image.
    source_path = tmp_path / "source.png"

    source_image = np.zeros(
        (10, 10, 3),
        dtype=np.uint8,
    )

    assert cv2.imwrite(str(source_path), source_image)

    # Keep the actual application image loader.
    original_loader = main.load_image

    def tracked_loader(path):
        events.append("load")
        return original_loader(path)

    monkeypatch.setattr(
        main,
        "load_image",
        tracked_loader,
    )

    # Simulate the selected operation without loading Real-ESRGAN.
    def test_enhancement(image):
        events.append("apply")

        assert np.array_equal(image, source_image)

        return image + 50

    monkeypatch.setitem(
        main.OPERATIONS,
        "Enhance the image ✦",
        test_enhancement,
    )

    storage = FakeStorage(events)
    application = main.Application(storage)

    # Execute the complete application workflow.
    result = application.process_image(
        path=str(source_path),
        operation="Enhance the image ✦",
        output_format="png",
    )

    # Verify that every stage was reached.
    assert "load" in events
    assert "apply" in events
    assert "save" in events

    # Verify that the stages happened in the correct order.
    assert events.index("load") < events.index("apply")
    assert events.index("apply") < events.index("save")

    # Verify that the processed image reached storage.
    assert np.array_equal(
        storage.saved_image,
        source_image + 50,
    )

    assert storage.saved_format == "png"
    assert result == "test-gallery/result.png"
