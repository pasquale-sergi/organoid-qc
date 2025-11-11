from pathlib import Path

# Paths
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Image settings
ALLOWED_FORMATS = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
THUMBNAIL_SIZE = (200, 200)
THUMBNAIL_QUALITY = 70

# ML thresholds (defaults)
DEFAULT_FOCUS_THRESHOLD = 150
DEFAULT_CONTRAST_THRESHOLD = 20
DEFAULT_EXPOSURE_MIN = 30
DEFAULT_EXPOSURE_MAX = 225

# Blur detection
BLUR_FOCUS_THRESHOLD = 80
BLUR_CONTRAST_THRESHOLD = 20