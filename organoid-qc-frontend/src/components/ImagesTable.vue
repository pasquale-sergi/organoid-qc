<template>
  <div class="images-section">
    <div class="section-header">
      <h3>🖼️ Images ({{ filteredImages.length }})</h3>
      <div class="filter-controls">
        <label class="filter-label">
          <input v-model="filterMlReady" type="checkbox" />
          ML-Ready Only
        </label>
      </div>
    </div>

    <div class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Filename</th>
            <th>Focus</th>
            <th>Contrast</th>
            <th>Exposure</th>
            <th>Diameter</th>
            <th>Circularity</th>
            <th>Status</th>
            <th>Reason</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="img in filteredImages"
            :key="img.id"
            @click="openPreview(img)"
            class="clickable-row"
            :class="{ 'row-ready': img.is_ml_ready, 'row-rejected': !img.is_ml_ready }"
          >
            <td class="filename">{{ img.filename }}</td>
            <td>
              <span :class="`quality-${getQuality(img.focus_score, 'focus')}`">
                {{ img.focus_score }}
              </span>
            </td>
            <td>
              <span :class="`quality-${getQuality(img.contrast_level, 'contrast')}`">
                {{ img.contrast_level }}
              </span>
            </td>
            <td>
              <span :class="`quality-${getQuality(img.exposure_level, 'exposure')}`">
                {{ img.exposure_level }}
              </span>
            </td>
            <td>{{ img.organoid_diameter ? img.organoid_diameter.toFixed(1) : "-" }}</td>
            <td>{{ img.organoid_shape_regularity ? img.organoid_shape_regularity.toFixed(2) : "-" }}</td>
            <td>
              <span :class="`status-${img.is_ml_ready ? 'ready' : 'rejected'}`">
                {{ img.is_ml_ready ? "✓ Ready" : "✗ Rejected" }}
              </span>
            </td>
            <td class="reason">{{ img.quality_reason }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Image Preview Modal -->
    <ImagePreview 
      :image="selectedImage" 
      :is-open="showPreview"
      @close="showPreview = false"
    />

    <div v-if="filteredImages.length === 0" class="empty-message">
      No images match the current filters
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import ImagePreview from "./ImagePreview.vue";

const props = defineProps({
  images: {
    type: Array,
    required: true
  },
  thresholds: {
    type: Object,
    required: true
  }
});

const filterMlReady = ref(false);
const showPreview = ref(false);
const selectedImage = ref(null);

const openPreview = (image) => {
  selectedImage.value = image;
  showPreview.value = true;
};

const getQuality = (value, type) => {
  if (type === "focus") {
    if (value >= 150) return "good";
    if (value >= 80) return "warning";
    return "bad";
  }
  if (type === "contrast") {
    if (value >= 40) return "good";
    if (value >= 20) return "warning";
    return "bad";
  }
  if (type === "exposure") {
    if (value >= 50 && value <= 200) return "good";
    if (value >= 30 && value <= 225) return "warning";
    return "bad";
  }
  return "";
};

const filteredImages = computed(() => {
  let result = props.images.map((img) => {
    const issues = [];

    if (img.focus_score < props.thresholds.focus) {
      issues.push("focus_too_low");
    }
    if (img.contrast_level < props.thresholds.contrast) {
      issues.push("contrast_too_low");
    }
    if (
      img.exposure_level < props.thresholds.exposure_min ||
      img.exposure_level > props.thresholds.exposure_max
    ) {
      issues.push("exposure_problem");
    }

    return {
      ...img,
      is_ml_ready: issues.length === 0,
      quality_reason: issues.length > 0 ? issues.join(", ") : "passed_all_checks"
    };
  });

  if (filterMlReady.value) {
    result = result.filter((img) => img.is_ml_ready);
  }

  return result;
});
</script>

<style scoped>
.images-section {
  margin-top: 24px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h3 {
  margin: 0;
  color: #333;
}

.filter-controls {
  display: flex;
  gap: 12px;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-weight: 500;
  color: #333;
}

.table-wrapper {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow-x: auto;
  max-height: 600px;
  overflow-y: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

table th {
  background: #f8f9fa;
  padding: 12px;
  text-align: left;
  font-weight: 600;
  border-bottom: 2px solid #e0e0e0;
  color: #555;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  position: sticky;
  top: 0;
}

table td {
  padding: 12px;
  border-bottom: 1px solid #e0e0e0;
}

.clickable-row {
  cursor: pointer;
  transition: all 0.2s ease;
}

.clickable-row:hover {
  background: #e7f0ff !important;
  box-shadow: inset 0 0 0 2px #0066cc;
}

table tr.row-ready {
  background: #f0fff4;
}

table tr.row-rejected {
  background: #fff5f5;
}

.filename {
  font-family: 'Monaco', 'Menlo', monospace;
  font-size: 0.85rem;
  color: #666;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.quality-good {
  color: #28a745;
  font-weight: 600;
}

.quality-warning {
  color: #ffc107;
  font-weight: 600;
}

.quality-bad {
  color: #dc3545;
  font-weight: 600;
}

.status-ready {
  background: #d4edda;
  color: #155724;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
}

.status-rejected {
  background: #f8d7da;
  color: #721c24;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
}

.reason {
  font-size: 0.8rem;
  color: #666;
  max-width: 150px;
}

.empty-message {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  font-style: italic;
}
</style>