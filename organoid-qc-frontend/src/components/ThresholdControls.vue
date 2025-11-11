<template>
  <div class="threshold-controls">
    <h3>⚙️ Adjust Quality Thresholds</h3>

    <div class="control-group">
      <label>Focus Score Threshold</label>
      <div class="slider-container">
        <input
          v-model.number="localThresholds.focus"
          type="range"
          min="0"
          max="200"
          @input="emitUpdate"
        />
        <span class="value">{{ localThresholds.focus }}</span>
      </div>
      <p class="hint">Minimum focus score for ML readiness</p>
    </div>

    <div class="control-group">
      <label>Contrast Threshold</label>
      <div class="slider-container">
        <input
          v-model.number="localThresholds.contrast"
          type="range"
          min="0"
          max="100"
          @input="emitUpdate"
        />
        <span class="value">{{ localThresholds.contrast }}</span>
      </div>
      <p class="hint">Minimum contrast level</p>
    </div>

    <div class="control-group">
      <label>Exposure Range</label>
      <div class="range-inputs">
        <input
          v-model.number="localThresholds.exposure_min"
          type="number"
          min="0"
          max="255"
          @input="emitUpdate"
        />
        <span class="separator">to</span>
        <input
          v-model.number="localThresholds.exposure_max"
          type="number"
          min="0"
          max="255"
          @input="emitUpdate"
        />
      </div>
      <p class="hint">Valid exposure range (0-255)</p>
    </div>

    <button @click="resetToDefaults" class="btn-reset">
      ↻ Reset to Defaults
    </button>
  </div>
</template>

<script setup>
import { reactive, watch } from "vue";

const props = defineProps({
  thresholds: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(["update"]);

const localThresholds = reactive({ ...props.thresholds });

watch(
  () => props.thresholds,
  (newThresholds) => {
    Object.assign(localThresholds, newThresholds);
  },
  { deep: true }
);

const emitUpdate = () => {
  emit("update", { ...localThresholds });
};

const resetToDefaults = () => {
  Object.assign(localThresholds, {
    focus: 80,
    contrast: 20,
    exposure_min: 30,
    exposure_max: 225
  });
  emitUpdate();
};
</script>

<style scoped>
.threshold-controls {
  background: linear-gradient(135deg, #f0f4f8 0%, #e8ecf1 100%);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  border-left: 4px solid #0066cc;
}

.threshold-controls h3 {
  margin-top: 0;
  margin-bottom: 16px;
  color: #333;
}

.control-group {
  margin-bottom: 20px;
}

.control-group label {
  display: block;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.slider-container {
  display: flex;
  gap: 12px;
  align-items: center;
}

.slider-container input {
  flex: 1;
  height: 6px;
  padding: 0;
}

.value {
  min-width: 50px;
  text-align: right;
  font-weight: 700;
  color: #0066cc;
  font-size: 1.1rem;
}

.range-inputs {
  display: flex;
  gap: 12px;
  align-items: center;
}

.range-inputs input {
  width: 100px;
  padding: 8px;
}

.separator {
  color: #666;
  font-weight: 500;
}

.hint {
  font-size: 0.8rem;
  color: #999;
  margin-top: 4px;
  margin-bottom: 0;
}

.btn-reset {
  width: 100%;
  padding: 10px;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-reset:hover {
  background: #5a6268;
}

@media (max-width: 768px) {
  .range-inputs {
    flex-direction: column;
    align-items: flex-start;
  }

  .range-inputs input {
    width: 100%;
  }
}
</style>