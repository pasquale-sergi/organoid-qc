from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from services.analysis import calculate_batch_statistics, detect_equipment_issues

router = APIRouter(prefix="/experiments", tags=["batch"])

@router.get("/{exp_id}/batch-report")
def get_batch_report(
    exp_id: int,
    focus_threshold: float = 150,
    contrast_threshold: float = 20,
    exposure_min: float = 30,
    exposure_max: float = 225,
    db: Session = Depends(get_db)
):
    """Get batch report with custom thresholds"""
    images = db.execute(text("""
        SELECT focus_score, contrast_level, exposure_level, 
               imaging_session_id, is_ml_ready, quality_reason
        FROM images 
        WHERE experiment_id = :id
    """), {"id": exp_id}).fetchall()

    if not images:
        return {
            "total_images": 0,
            "ml_ready_images": 0,
            "pass_rate": 0,
            "avg_focus": 0,
            "avg_contrast": 0,
            "avg_exposure": 0,
            "sessions": {}
        }

    total = len(images)
    
    # Calculate averages
    avg_focus = sum(img.focus_score for img in images) / total if images else 0
    avg_contrast = sum(img.contrast_level for img in images) / total if images else 0
    avg_exposure = sum(img.exposure_level for img in images) / total if images else 0
    
    # Count ML-ready
    ml_ready = sum(1 for img in images if img.focus_score >= focus_threshold 
                   and img.contrast_level >= contrast_threshold
                   and exposure_min <= img.exposure_level <= exposure_max)
    
    # Group by imaging session
    sessions = {}
    for img in images:
        session = img.imaging_session_id or "unknown"
        if session not in sessions:
            sessions[session] = {"total": 0, "ready": 0, "issues": []}
        sessions[session]["total"] += 1
        
        # Check if image passes thresholds
        is_ready = (img.focus_score >= focus_threshold 
                   and img.contrast_level >= contrast_threshold
                   and exposure_min <= img.exposure_level <= exposure_max)
        
        if is_ready:
            sessions[session]["ready"] += 1
        else:
            sessions[session]["issues"].append(img.quality_reason or "unknown_issue")

    return {
        "total_images": total,
        "ml_ready_images": ml_ready,
        "pass_rate": round((ml_ready / total) * 100, 2) if total > 0 else 0,
        "avg_focus": round(avg_focus, 2),
        "avg_contrast": round(avg_contrast, 2),
        "avg_exposure": round(avg_exposure, 2),
        "applied_thresholds": {
            "focus": focus_threshold,
            "contrast": contrast_threshold,
            "exposure": f"{exposure_min}-{exposure_max}"
        },
        "sessions": sessions
    }

@router.get("/{exp_id}/images")
def get_images(exp_id: int, db: Session = Depends(get_db)):
    """Get all images for experiment with quality metrics"""
    images = db.execute(text("""
        SELECT id, filename, focus_score, contrast_level, exposure_level,
               is_ml_ready, quality_reason, organoid_diameter,
               organoid_shape_regularity, imaging_session_id, microscope_id,
               operator_id
        FROM images
        WHERE experiment_id = :id
        ORDER BY created_at DESC
    """), {"id": exp_id}).fetchall()
    
    return [
        {
            "id": img.id,
            "filename": img.filename,
            "focus_score": round(img.focus_score, 2),
            "contrast_level": round(img.contrast_level, 2),
            "exposure_level": round(img.exposure_level, 2),
            "is_ml_ready": img.is_ml_ready,
            "quality_reason": img.quality_reason,
            "organoid_diameter": round(img.organoid_diameter, 2) if img.organoid_diameter else None,
            "organoid_shape_regularity": round(img.organoid_shape_regularity, 2) if img.organoid_shape_regularity else None,
            "imaging_session_id": img.imaging_session_id,
            "microscope_id": img.microscope_id,
            "operator_id": img.operator_id,
        }
        for img in images
    ]

@router.get("/{exp_id}/equipment-health")
def equipment_health(exp_id: int, db: Session = Depends(get_db)):
    """Detect equipment issues from imaging patterns"""
    images = db.execute(text("""
        SELECT microscope_id, focus_score, created_at
        FROM images
        WHERE experiment_id = :id
        ORDER BY microscope_id, created_at ASC
    """), {"id": exp_id}).fetchall()
    
    if not images:
        return {"status": "no_data"}
    
    # Group by microscope
    microscopes = {}
    for img in images:
        if img.microscope_id not in microscopes:
            microscopes[img.microscope_id] = []
        microscopes[img.microscope_id].append(img.focus_score)
    
    # Calculate trend for each microscope
    results = {}
    for micro_id, scores in microscopes.items():
        if len(scores) < 2:
            results[micro_id] = {"status": "insufficient_data", "total": len(scores)}
        else:
            trend = (scores[-1] - scores[0]) / len(scores)
            issues = []
            
            if trend < -5:
                issues.append("⚠️ Focus degradation detected")
            
            # Count low focus images
            low_focus_count = sum(1 for s in scores if s < 50)
            if low_focus_count > 0:
                pct = round((low_focus_count / len(scores)) * 100, 1)
                issues.append(f"⚠️ {low_focus_count}/{len(scores)} images have focus < 50 ({pct}%)")
            
            results[micro_id] = {
                "microscope": micro_id,
                "total_images": len(scores),
                "focus_trend": round(trend, 2),
                "issues": issues or ["✓ Normal"]
            }
    
    return results