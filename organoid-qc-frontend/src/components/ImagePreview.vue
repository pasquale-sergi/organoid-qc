<script setup>
import { ref, computed, watch, onMounted } from "vue";

const props = defineProps({
  image: {
    type: Object,
    default: null
  },
  isOpen: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(["close"]);
const loading = ref(false);
const imageError = ref(false);
const loadTimeout = ref(null);

const imageUrl = computed(() => {
  if (!props.image?.id) return null;
  return `http://localhost:8000/images/${props.image.id}`;
});

const onImageLoad = () => {
  loading.value = false;
  if (loadTimeout.value) clearTimeout(loadTimeout.value);
};

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    loading.value = true;
    imageError.value = false;
    loadTimeout.value = setTimeout(() => {
      if (loading.value) {
        loading.value = false;
        imageError.value = true;
      }
    }, 5000);
  } else {
    if (loadTimeout.value) clearTimeout(loadTimeout.value);
  }
});

const close = () => {
  if (loadTimeout.value) clearTimeout(loadTimeout.value);
  emit("close");
};

const onImageError = () => {
  loading.value = false;
  imageError.value = true;
  if (loadTimeout.value) clearTimeout(loadTimeout.value);
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
</script>

<template>
  <teleport to="body">
    <transition name="fade">
      <div v-if="isOpen" class="modal-overlay" @click="close">
        <div class="modal-card" @click.stop>
          <button class="close-btn" @click="close">✕</button>
          
          <div class="modal-header">
            <h2>{{ image.filename }}</h2>
          </div>
          
          <div class="modal-body">
            <!-- Image Preview -->
            <div class="image-container">
              <img 
                v-if="image.id" 
                :src="imageUrl" 
                class="preview-image"
                :style="{ opacity: loading ? 0.5 : 1 }"  
                @load="() => { loading = false; if (loadTimeout.value) clearTimeout(loadTimeout.value); }"
                @error="onImageError"
                alt="Preview"
              />
              
              <!-- Show spinner overlay while loading -->
              <div v-if="loading" class="loading-spinner-overlay">
                <div class="spinner"></div>
                <p>Loading image...</p>
              </div>
              
              <!-- Show error if failed -->
              <div v-else-if="imageError" class="error-message">
                <p>❌ Failed to load image</p>
                <small>Image file may not be available. Please re-upload images.</small>
              </div>
              
              <div v-else-if="!image.id" class="no-image">No image available</div>
            </div>

            <!-- Image Details -->
            <div class="image-details">
              <div class="details-grid">
                <div class="detail-item">
                  <span class="label">Focus Score</span>
                  <span class="value" :class="`quality-${getQuality(image.focus_score, 'focus')}`">
                    {{ image.focus_score }}
                  </span>
                </div>
                <div class="detail-item">
                  <span class="label">Contrast</span>
                  <span class="value" :class="`quality-${getQuality(image.contrast_level, 'contrast')}`">
                    {{ image.contrast_level }}
                  </span>
                </div>
                <div class="detail-item">
                  <span class="label">Exposure</span>
                  <span class="value" :class="`quality-${getQuality(image.exposure_level, 'exposure')}`">
                    {{ image.exposure_level }}
                  </span>
                </div>
                <div class="detail-item">
                  <span class="label">Diameter (μm)</span>
                  <span class="value">{{ image.organoid_diameter ? image.organoid_diameter.toFixed(1) : "—" }}</span>
                </div>
                <div class="detail-item">
                  <span class="label">Circularity</span>
                  <span class="value">{{ image.organoid_shape_regularity ? image.organoid_shape_regularity.toFixed(2) : "—" }}</span>
                </div>
                <div class="detail-item">
                  <span class="label">Status</span>
                  <span :class="`status-${image.is_ml_ready ? 'ready' : 'rejected'}`">
                    {{ image.is_ml_ready ? "✓ Ready" : "✗ Rejected" }}
                  </span>
                </div>
              </div>

              <div class="reason-box">
                <span class="label">Quality Reason</span>
                <p>{{ image.quality_reason }}</p>
              </div>
            </div>
          </div>

          <div class="modal-footer">
            <button @click="close" class="btn-secondary">Close</button>
          </div>
        </div>
      </div>
    </transition>
  </teleport>
</template>

<style scoped>
/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

/* Modal Card */
.modal-card {
  background: white;
  border-radius: 12px;
  max-width: 700px;
  width: 100%;
  max-height: 85vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: #f0f0f0;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: #e0e0e0;
  transform: rotate(90deg);
}

/* Modal Header */
.modal-header {
  padding: 20px 24px;
  border-bottom: 2px solid #e0e0e0;
  position: relative;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.3rem;
  word-break: break-word;
  padding-right: 40px;
}

/* Modal Body */
.modal-body {
  overflow-y: auto;
  flex: 1;
  padding: 24px;
}

.image-container {
  margin-bottom: 24px;
  border-radius: 8px;
  overflow: hidden;
  background: #f8f9fa;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.preview-image {
  width: 100%;
  height: auto;
  max-height: 400px;
  object-fit: contain;
}

.no-image {
  width: 100%;
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-style: italic;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.loading-spinner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  border-radius: 8px;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e0e0e0;
  border-top-color: #0066cc;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Details Grid */
.image-details {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.error-message {
  width: 100%;
  height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #dc3545;
  text-align: center;
  gap: 8px;
}

.error-message p {
  margin: 0;
  font-weight: 600;
}

.error-message small {
  color: #999;
  font-size: 0.85rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.label {
  font-size: 0.75rem;
  color: #666;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.4px;
}

.value {
  font-size: 1rem;
  font-weight: 700;
  color: #0066cc;
}

.quality-good {
  color: #28a745;
}

.quality-warning {
  color: #ffc107;
}

.quality-bad {
  color: #dc3545;
}

.status-ready {
  background: #d4edda;
  color: #155724;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  width: fit-content;
}

.status-rejected {
  background: #f8d7da;
  color: #721c24;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 600;
  width: fit-content;
}

.reason-box {
  margin-top: 12px;
  padding: 12px;
  background: white;
  border-radius: 6px;
  border-left: 3px solid #0066cc;
}

.reason-box .label {
  display: block;
  margin-bottom: 6px;
}

.reason-box p {
  margin: 0;
  color: #555;
  font-size: 0.9rem;
}

/* Modal Footer */
.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #e0e0e0;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-secondary {
  padding: 10px 20px;
  background: #6c757d;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-secondary:hover {
  background: #5a6268;
}

/* Responsive */
@media (max-width: 600px) {
  .modal-card {
    max-width: 95vw;
    max-height: 95vh;
  }

  .details-grid {
    grid-template-columns: 1fr 1fr;
  }

  .modal-body {
    padding: 16px;
  }
}
</style>