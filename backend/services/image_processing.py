import cv2
import numpy as np
from PIL import Image
import io
from fastapi import HTTPException, status

def compute_focus_score(image_bytes: bytes) -> float:
    """Laplacian variance for focus detection"""
    try:
        arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("Invalid image format")
        return float(cv2.Laplacian(img, cv2.CV_64F).var())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image processing failed: {str(e)}"
        )

def compute_contrast_level(image_bytes: bytes) -> float:
    """Calculate contrast using standard deviation"""
    try:
        arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return 0.0
        return float(img.std())
    except:
        return 0.0

def compute_exposure_level(image_bytes: bytes) -> float:
    """Calculate exposure using mean pixel intensity"""
    try:
        arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return 0.0
        return float(img.mean())
    except:
        return 0.0

def estimate_organoid_properties(image_bytes: bytes) -> tuple:
    """Estimate organoid diameter and circularity"""
    try:
        arr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None, None
        
        _, thresh = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        
        if not contours:
            return None, None
        
        contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        diameter = 2 * np.sqrt(area / np.pi)
        circularity = (4 * np.pi * area) / (perimeter ** 2 + 1e-5)
        
        return float(diameter), float(circularity)
    except:
        return None, None

def get_image_dimensions(image_bytes: bytes) -> tuple:
    """Get image width and height"""
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        return None, None
    return img.shape[1], img.shape[0]

def create_thumbnail(image_bytes: bytes, size=(200, 200)) -> bytes:
    """Create thumbnail from image bytes"""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        thumb_io = io.BytesIO()
        img.save(thumb_io, format='JPEG', quality=70)
        thumb_io.seek(0)
        return thumb_io.getvalue()
    except Exception as e:
        print(f"Thumbnail creation failed: {e}")
        return None