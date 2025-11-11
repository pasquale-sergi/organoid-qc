from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from pathlib import Path

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/images/{image_id}")
def debug_image(image_id: int, db: Session = Depends(get_db)):
    """Debug endpoint to check image data"""
    image = db.execute(
        text("SELECT id, filename, file_path, thumbnail_path FROM images WHERE id = :id"),
        {"id": image_id}
    ).first()
    
    if not image:
        return {"error": "Image not found"}
    
    file_exists = Path(image.file_path).exists() if image.file_path else False
    
    return {
        "id": image.id,
        "filename": image.filename,
        "file_path": image.file_path,
        "file_exists": file_exists,
        "abs_path": str(Path(image.file_path).absolute()) if image.file_path else None
    }

@router.post("/clear-images")
def clear_images(db: Session = Depends(get_db)):
    """Clear all images - TEMPORARY (use with caution)"""
    try:
        db.execute(text("DELETE FROM images"))
        db.commit()
        return {"message": "All images cleared", "status": "success"}
    except Exception as e:
        return {"message": str(e), "status": "error"}

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Check database and API health"""
    try:
        db.execute(text("SELECT 1"))
        return {
            "api": "ok",
            "database": "ok",
            "timestamp": __import__("datetime").datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "api": "ok",
            "database": "error",
            "error": str(e)
        }