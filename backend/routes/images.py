from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from pathlib import Path
from database import get_db
from config import ALLOWED_FORMATS
from services.image_processing import (
    compute_focus_score, compute_contrast_level, compute_exposure_level,
    estimate_organoid_properties, get_image_dimensions, create_thumbnail
)
from services.storage import save_image_file, save_thumbnail_file
from services.analysis import determine_ml_readiness

router = APIRouter(tags=["images"])

@router.post("/upload/{experiment_id}", status_code=status.HTTP_201_CREATED)  # ← CHANGED: added /upload to route
async def upload_img(
    experiment_id: int,
    file: UploadFile = File(...),
    imaging_session_id: str = Form(...),  
    microscope_id: str = Form(...),       
    operator_id: str = Form(None),       
    db: Session = Depends(get_db)
):
    """Upload and process microscopy image"""
    print(f"📨 Received file: {file.filename}")  
    print(f"   Size: {file.size if file.size else 'unknown'}")
    print(f"   Content-type: {file.content_type}")
    
    if not file.filename.lower().endswith(ALLOWED_FORMATS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Supported formats: {', '.join(ALLOWED_FORMATS)}"
        )
    
    exp_check = db.execute(
        text("SELECT id FROM experiments WHERE id = :id"),
        {"id": experiment_id}
    ).scalar()
    if not exp_check:
        raise HTTPException(status_code=404, detail="Experiment not found")

    contents = await file.read()
    
    # Compute metrics
    focus = compute_focus_score(contents)
    contrast = compute_contrast_level(contents)
    exposure = compute_exposure_level(contents)
    width, height = get_image_dimensions(contents)
    diameter, circularity = estimate_organoid_properties(contents)
    is_ml_ready, quality_reason = determine_ml_readiness(focus, contrast, exposure)

    # Save files
    original_path = save_image_file(experiment_id, file.filename, contents)
    thumb_bytes = create_thumbnail(contents)
    thumb_path = save_thumbnail_file(experiment_id, file.filename, thumb_bytes)

    # Save to database
    result = db.execute(
        text("""
            INSERT INTO images (
                experiment_id, filename, focus_score, contrast_level,
                exposure_level, is_ml_ready, quality_reason, organoid_diameter,
                organoid_shape_regularity, imaging_session_id, microscope_id,
                operator_id, acquisition_time, width, height, file_path, thumbnail_path
            )
            VALUES (
                :exp_id, :fname, :focus, :contrast, :exposure, :ml_ready,
                :reason, :diameter, :circularity, :session_id, :micro_id,
                :op_id, :acq_time, :width, :height, :file_path, :thumb_path
            )
            RETURNING id
        """),
        {
            "exp_id": experiment_id,
            "fname": file.filename,
            "focus": focus,
            "contrast": contrast,
            "exposure": exposure,
            "ml_ready": is_ml_ready,
            "reason": quality_reason,
            "diameter": diameter,
            "circularity": circularity,
            "session_id": imaging_session_id,
            "micro_id": microscope_id,
            "op_id": operator_id,
            "acq_time": datetime.now(),
            "width": width,
            "height": height,
            "file_path": str(original_path),
            "thumb_path": str(thumb_path) if thumb_path else None
        }
    )
    
    image_id = result.scalar()
    db.commit()

    return {
        "id": image_id,
        "focus_score": round(focus, 2),
        "contrast_level": round(contrast, 2),
        "exposure_level": round(exposure, 2),
        "is_ml_ready": is_ml_ready,
        "quality_reason": quality_reason,
        "organoid_diameter": round(diameter, 2) if diameter else None,
        "organoid_circularity": round(circularity, 2) if circularity else None,
        "dimensions": {"width": width, "height": height}
    }
@router.get("/images/{image_id}")
def get_image(image_id: int, db: Session = Depends(get_db)):
    """Get full image as file"""
    print(f"\n🔍 GET /images/{image_id} called") 
    try:
        image = db.execute(
            text("SELECT file_path FROM images WHERE id = :id"),
            {"id": image_id}
        ).first()
        
        if not image or not image.file_path:
            print(f"❌ Image {image_id} not found in DB")  
            raise HTTPException(status_code=404, detail="Image not found")
        
        file_path = Path(image.file_path)
        print(f"  DB path: {file_path}") 
        
        if not file_path.is_absolute():
            file_path = Path(__file__).parent.parent / file_path
        
        file_path = file_path.resolve()
        print(f"  Resolved: {file_path}")  
        print(f"  Exists: {file_path.exists()}")  
        
        if not file_path.exists():
            print(f"✗ File not found at: {file_path}")
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        print(f"✓ Serving: {file_path}\n")
        return FileResponse(str(file_path))
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Error: {e}\n")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/images/{image_id}/thumbnail")
def get_thumbnail(image_id: int, db: Session = Depends(get_db)):
    """Get thumbnail as file"""
    image = db.execute(
        text("SELECT thumbnail_path FROM images WHERE id = :id"),
        {"id": image_id}
    ).first()
    
    if not image or not image.thumbnail_path:
        raise HTTPException(status_code=404, detail="Thumbnail not found")
    
    thumb_path = Path(image.thumbnail_path)
    
    if not thumb_path.is_absolute():
        thumb_path = Path(__file__).parent.parent / thumb_path
    
    thumb_path = thumb_path.resolve()
    
    if not thumb_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(str(thumb_path), media_type="image/jpeg")