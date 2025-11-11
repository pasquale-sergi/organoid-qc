import { reactive, computed } from "vue";

export function useThresholds() {
  const thresholds = reactive({
    focus: 80,
    contrast: 20,
    exposure_min: 30,
    exposure_max: 225
  });

  const getQualityClass = (value, type) => {
    if (type === "focus") {
      if (value >= 150) return "quality-good";
      if (value >= 80) return "quality-warning";
      return "quality-bad";
    }
    if (type === "contrast") {
      if (value >= 40) return "quality-good";
      if (value >= 20) return "quality-warning";
      return "quality-bad";
    }
    if (type === "exposure") {
      if (value >= 50 && value <= 200) return "quality-good";
      if (value >= 30 && value <= 225) return "quality-warning";
      return "quality-bad";
    }
    return "";
  };

  const calculateImageQuality = (image) => {
    const issues = [];

    if (image.focus_score < thresholds.focus) {
      issues.push("focus_too_low");
    }
    if (image.contrast_level < thresholds.contrast) {
      issues.push("contrast_too_low");
    }
    if (
      image.exposure_level < thresholds.exposure_min ||
      image.exposure_level > thresholds.exposure_max
    ) {
      issues.push("exposure_problem");
    }

    return {
      is_ml_ready: issues.length === 0,
      quality_reason: issues.length > 0 ? issues.join(", ") : "passed_all_checks"
    };
  };

  return {
    thresholds,
    getQualityClass,
    calculateImageQuality
  };
}