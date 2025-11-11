from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from datetime import datetime
import csv
from io import StringIO

router = APIRouter(prefix="/experiments", tags=["exports"])

@router.get("/{exp_id}/export-ml-ready")
def export_ml_ready(exp_id: int, db: Session = Depends(get_db)):
    """Export metadata for ML-ready images"""
    images = db.execute(
        text("""
            SELECT id, filename, focus_score, contrast_level, exposure_level,
                   organoid_diameter, organoid_shape_regularity,
                   imaging_session_id, microscope_id
            FROM images
            WHERE experiment_id = :id AND is_ml_ready = 1
            ORDER BY focus_score DESC
        """),
        {"id": exp_id}
    ).fetchall()

    if not images:
        raise HTTPException(status_code=404, detail="No ML-ready images")

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Filename", "Focus Score", "Contrast", "Exposure",
        "Organoid Diameter", "Circularity", "Imaging Session", "Microscope"
    ])
    for img in images:
        writer.writerow([
            img.filename, round(img.focus_score, 2),
            round(img.contrast_level, 2), round(img.exposure_level, 2),
            round(img.organoid_diameter, 2) if img.organoid_diameter else "",
            round(img.organoid_shape_regularity, 2) if img.organoid_shape_regularity else "",
            img.imaging_session_id, img.microscope_id
        ])

    return {
        "csv": output.getvalue(),
        "ml_ready_count": len(images),
        "filename": f"ml_ready_images_{exp_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    }

@router.get("/{exp_id}/export")
def export_all(exp_id: int, db: Session = Depends(get_db)):
    """Export all images metadata"""
    images = db.execute(
        text("""
            SELECT filename, focus_score, contrast_level, exposure_level,
                   is_ml_ready, quality_reason, organoid_diameter,
                   organoid_shape_regularity, imaging_session_id, microscope_id,
                   created_at
            FROM images
            WHERE experiment_id = :id
            ORDER BY created_at
        """),
        {"id": exp_id}
    ).fetchall()

    if not images:
        raise HTTPException(status_code=404, detail="No images to export")

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Filename", "Focus Score", "Contrast", "Exposure", "Status",
        "Quality Reason", "Organoid Diameter", "Circularity",
        "Imaging Session", "Microscope", "Created At"
    ])
    for img in images:
        writer.writerow([
            img.filename, round(img.focus_score, 2),
            round(img.contrast_level, 2), round(img.exposure_level, 2),
            "Ready" if img.is_ml_ready else "Rejected",
            img.quality_reason, 
            round(img.organoid_diameter, 2) if img.organoid_diameter else "",
            round(img.organoid_shape_regularity, 2) if img.organoid_shape_regularity else "",
            img.imaging_session_id, img.microscope_id, img.created_at
        ])

    return {
        "csv": output.getvalue(),
        "total_count": len(images),
        "filename": f"all_images_{exp_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    }

@router.get("/{exp_id}/generate-copy-script")
def generate_copy_script(
    exp_id: int,
    focus_threshold: float = 150,
    contrast_threshold: float = 20,
    exposure_min: float = 30,
    exposure_max: float = 225,
    db: Session = Depends(get_db)
):
    """Generate Python script to organize ML-ready images locally"""
    images = db.execute(text("""
        SELECT filename, focus_score, contrast_level, exposure_level
        FROM images 
        WHERE experiment_id = :id
        ORDER BY focus_score DESC
    """), {"id": exp_id}).fetchall()
    
    # Filter ML-ready
    ml_ready_files = []
    for img in images:
        issues = []
        if img.focus_score < focus_threshold:
            issues.append("focus_too_low")
        if img.contrast_level < contrast_threshold:
            issues.append("contrast_too_low")
        if img.exposure_level < exposure_min or img.exposure_level > exposure_max:
            issues.append("exposure_problem")
        
        if not issues:
            ml_ready_files.append(img.filename)
    
    script = f"""#!/usr/bin/env python3
\"\"\"
OrganoidQC ML-Ready Image Organizer
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Experiment ID: {exp_id}

Quality Thresholds:
  - Focus Score: >= {focus_threshold}
  - Contrast: >= {contrast_threshold}
  - Exposure: {exposure_min}-{exposure_max}

ML-Ready Images: {len(ml_ready_files)}/{len(images)}
\"\"\"

import os
import shutil
from pathlib import Path

# Configuration
SOURCE_DIR = input("Enter path to source images directory: ").strip()
OUTPUT_DIR = input("Enter output directory name (default: ml_ready_images): ").strip() or "ml_ready_images"

if not os.path.exists(SOURCE_DIR):
    print(f"Error: Source directory not found: {{SOURCE_DIR}}")
    exit(1)

# ML-ready filenames
ML_READY_FILES = [
"""
    
    for filename in ml_ready_files:
        script += f'    "{filename}",\n'
    
    script += f"""]

# Statistics
TOTAL_IMAGES = {len(images)}
READY_IMAGES = {len(ml_ready_files)}
REJECTED_IMAGES = {len(images) - len(ml_ready_files)}

# Create output directory
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# Copy ML-ready images
copied = 0
failed = 0

print(f"\\nStarting copy process...")
print(f"Source: {{SOURCE_DIR}}")
print(f"Destination: {{OUTPUT_DIR}}")
print(f"Images to copy: {{len(ML_READY_FILES)}}\\n")

for filename in ML_READY_FILES:
    src = os.path.join(SOURCE_DIR, filename)
    dst = os.path.join(OUTPUT_DIR, filename)
    
    try:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            copied += 1
            print(f"  ✓ {{filename}}")
        else:
            failed += 1
            print(f"  ✗ NOT FOUND: {{filename}}")
    except Exception as e:
        failed += 1
        print(f"  ✗ ERROR: {{filename}} - {{str(e)}}")

# Summary
print(f"\\n{{'='*60}}")
print(f"Summary:")
print(f"  Total images in experiment: {{TOTAL_IMAGES}}")
print(f"  ML-ready images: {{READY_IMAGES}} ({{(READY_IMAGES/TOTAL_IMAGES)*100:.1f}}%)")
print(f"  Rejected images: {{REJECTED_IMAGES}}")
print(f"\\n  Copied: {{copied}}")
print(f"  Failed: {{failed}}")
print(f"\\nOutput directory: {{os.path.abspath(OUTPUT_DIR)}}")
print(f"{{'='*60}}")

if failed == 0:
    print("✓ All images copied successfully!")
else:
    print(f"⚠ {{failed}} images could not be copied. Check paths and try again.")
"""