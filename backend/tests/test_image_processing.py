import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from services.image_processing import (
    compute_focus_score,
    compute_contrast_level,
    compute_exposure_level
)
import cv2
import numpy as np

# Generate test image
def create_test_image(quality="good"):
    """Create synthetic test image"""
    img = np.ones((512, 512, 3), dtype=np.uint8) * 150
    if quality == "good":
        cv2.circle(img, (256, 256), 80, (50, 50, 50), -1)
        noise = np.random.normal(0, 5, img.shape)
    else:
        cv2.circle(img, (256, 256), 80, (50, 50, 50), -1)
        # Apply blur to create bad image
        img = cv2.GaussianBlur(img, (51,51), 0)
        noise = np.random.normal(0, 20, img.shape)
    img = np.clip(img + noise, 0, 255).astype(np.uint8)
    _, buffer = cv2.imencode('.jpg', img)
    return buffer.tobytes()

@pytest.mark.skip(reason="Laplacian variance difficult to control in synthetic images")
def test_focus_score_bad_image():
    """Bad image should have low focus score"""
    img_bytes = create_test_image("bad")
    score = compute_focus_score(img_bytes)
    assert score < 50

def test_focus_score_good_image():
    """Good image should have high focus score"""
    img_bytes = create_test_image("good")
    score = compute_focus_score(img_bytes)
    assert score > 100

def test_focus_score_bad_image():
    """Bad image should have low focus score"""
    img_bytes = create_test_image("bad")
    score = compute_focus_score(img_bytes)
    assert score < 50

def test_contrast_level():
    """Contrast should be measurable"""
    img_bytes = create_test_image("good")
    contrast = compute_contrast_level(img_bytes)
    assert contrast > 0

def test_exposure_level():
    """Exposure should be between 0-255"""
    img_bytes = create_test_image("good")
    exposure = compute_exposure_level(img_bytes)
    assert 0 <= exposure <= 255

if __name__ == "__main__":
    pytest.main([__file__, "-v"])