from pathlib import Path
from config import UPLOAD_DIR

def get_experiment_upload_dir(exp_id: int) -> Path:
    """Get experiment upload directory"""
    exp_dir = UPLOAD_DIR / f"experiment_{exp_id}"
    exp_dir.mkdir(parents=True, exist_ok=True)
    (exp_dir / "originals").mkdir(exist_ok=True)
    (exp_dir / "thumbnails").mkdir(exist_ok=True)
    return exp_dir