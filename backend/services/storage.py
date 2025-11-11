from pathlib import Path
from utils.paths import get_experiment_upload_dir

def save_image_file(exp_id: int, filename: str, contents: bytes) -> Path:
    """Save original image to disk"""
    exp_dir = get_experiment_upload_dir(exp_id)
    safe_filename = filename.replace("../", "").replace("..\\", "")
    original_path = exp_dir / "originals" / safe_filename
    
    with open(original_path, "wb") as f:
        f.write(contents)
    
    # Store relative path (from backend root)
    abs_original_path = original_path.resolve()
    backend_root = Path(__file__).parent.parent.resolve()
    relative_path = abs_original_path.relative_to(backend_root)
    print(f"✓ Saved original: {original_path}")
    print(f"  Relative path: {relative_path}")
    return relative_path
def save_thumbnail_file(exp_id: int, filename: str, thumb_bytes: bytes) -> Path:
    """Save thumbnail to disk"""
    if not thumb_bytes:
        return None
    
    exp_dir = get_experiment_upload_dir(exp_id)
    safe_filename = filename.replace("../", "").replace("..\\", "")
    thumb_filename = safe_filename.rsplit(".", 1)[0] + "_thumb.jpg"
    thumb_path = exp_dir / "thumbnails" / thumb_filename
    
    with open(thumb_path, "wb") as f:
        f.write(thumb_bytes)
    
    # Store relative path (from backend root)
    abs_thumb_path = thumb_path.resolve()
    backend_root = Path(__file__).parent.parent.resolve()
    relative_path = abs_thumb_path.relative_to(backend_root)
    print(f"✓ Saved thumbnail: {thumb_path}")
    print(f"  Relative path: {relative_path}")
    return relative_path