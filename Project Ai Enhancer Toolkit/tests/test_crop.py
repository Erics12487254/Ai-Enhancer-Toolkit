import sys
from pathlib import Path

import numpy as np
import pytest


APP_SOURCE = Path(__file__).resolve().parents[1] / "Project Ai Enhancer Toolkit"
sys.path.insert(0, str(APP_SOURCE))

from crop import crop_image


def test_crops_the_expected_400_by_400_region():
    image = np.zeros((500, 600, 3), dtype=np.uint8)
    image[100, 100] = (1, 2, 3)
    image[499, 499] = (4, 5, 6)

    result = crop_image(image)

    assert result.shape == (400, 400, 3)
    np.testing.assert_array_equal(result[0, 0], (1, 2, 3))
    np.testing.assert_array_equal(result[-1, -1], (4, 5, 6))


def test_rejects_an_image_that_is_too_small():
    image = np.zeros((499, 500, 3), dtype=np.uint8)

    with pytest.raises(ValueError, match="Minimum size is 500x500"):
        crop_image(image)


def test_rejects_a_non_numpy_input():
    with pytest.raises(TypeError, match="Input must be a NumPy array"):
        crop_image("photo.png")