def determine_ml_readiness(
    focus: float,
    contrast: float,
    exposure: float,
    focus_threshold: float = 80,
    contrast_threshold: float = 20,
    exposure_min: float = 30,
    exposure_max: float = 225
) -> tuple:
    """Determine if image is suitable for ML inference"""
    issues = []
    
    if focus < focus_threshold:
        issues.append("focus_too_low")
    if contrast < contrast_threshold:
        issues.append("contrast_too_low")
    if exposure < exposure_min or exposure > exposure_max:
        issues.append("exposure_problem")
    
    is_ready = len(issues) == 0
    reason = ", ".join(issues) if issues else "passed_all_checks"
    
    return is_ready, reason

def calculate_batch_statistics(images):
    """Calculate batch-level statistics"""
    if not images:
        return {}
    
    total = len(images)
    avg_focus = sum(img.focus_score for img in images) / total
    avg_contrast = sum(img.contrast_level for img in images) / total
    avg_exposure = sum(img.exposure_level for img in images) / total
    
    return {
        "total": total,
        "avg_focus": round(avg_focus, 2),
        "avg_contrast": round(avg_contrast, 2),
        "avg_exposure": round(avg_exposure, 2)
    }

def detect_equipment_issues(images):
    """Detect equipment degradation from trends"""
    if len(images) < 2:
        return []
    
    focus_scores = [img.focus_score for img in images]
    trend = (focus_scores[-1] - focus_scores[0]) / len(focus_scores)
    
    issues = []
    if trend < -5:
        issues.append("⚠️ Focus degradation detected")
    if any(s < 50 for s in focus_scores):
        issues.append("⚠️ Critical focus failures")
    
    return issues