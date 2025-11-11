<template>
  <div class="upload-section">
    <h3>📤 Upload Images</h3>

    <div class="metadata-fields">
      <input
        v-model="metadata.session"
        type="text"
        placeholder="Imaging Session ID (optional)"
      />
      <input
        v-model="metadata.microscope"
        type="text"
        placeholder="Microscope ID (optional)"
      />
      <input
        v-model="metadata.operator"
        type="text"
        placeholder="Operator ID (optional)"
      />
    </div>

    <div class="upload-zone" @click="$refs.fileInput.click()" @dragover.prevent @drop.prevent="handleDrop">
      <input
        ref="fileInput"
        type="file"
        multiple
        accept="image/*"
        @change="handleFileSelect"
        style="display: none"
      />
      <div v-if="!uploading" class="upload-prompt">
        <p>📁 Click to select images or drag and drop</p>
        <span class="hint">Supports JPG, PNG, BMP, TIFF</span>
      </div>
      <div v-else class="uploading">
        <div class="spinner"></div>
        <p>Uploading {{ uploadProgress }} / {{ totalFiles }} files...</p>
      </div>
    </div>

    <div v-if="fileCount > 0 && !uploading" class="file-summary">
      {{ fileCount }} image{{ fileCount !== 1 ? "s" : "" }} selected
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

defineProps({
  uploading: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(["upload"]);

const metadata = ref({
  session: "",
  microscope: "",
  operator: ""
});

const fileInput = ref(null);
const fileCount = ref(0);
const uploadProgress = ref(0);
const totalFiles = ref(0);

const handleFileSelect = (event) => {
  const files = Array.from(event.target.files);
  if (files.length > 0) {
    fileCount.value = files.length;
    totalFiles.value = files.length;
    uploadProgress.value = 0;
    emit("upload", files, metadata.value);
  }
};

const handleDrop = (event) => {
  const files = Array.from(event.dataTransfer.files);
  const imageFiles = files.filter(file => 
    file.type.startsWith('image/') || 
    /\.(jpg|jpeg|png|bmp|tiff?)$/i.test(file.name)
  );
  
  if (imageFiles.length > 0) {
    fileCount.value = imageFiles.length;
    totalFiles.value = imageFiles.length;
    uploadProgress.value = 0;
    emit("upload", imageFiles, metadata.value);
  }
};
</script>

<style scoped>
.upload-section {
  background: linear-gradient(135deg, #f0f4f8 0%, #e8ecf1 100%);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.upload-section h3 {
  margin-top: 0;
  margin-bottom: 16px;
  color: #333;
}

.metadata-fields {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.metadata-fields input {
  font-size: 0.9rem;
}

.upload-zone {
  border: 2px dashed #0066cc;
  border-radius: 8px;
  padding: 32px;
  text-align: center;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.upload-zone:hover {
  border-color: #004499;
  background: #f8f9fa;
}

.upload-zone.dragover {
  border-color: #28a745;
  background: #f0fff4;
}

.upload-prompt {
  pointer-events: none;
}

.upload-prompt p {
  margin: 0;
  color: #0066cc;
  font-weight: 600;
  margin-bottom: 8px;
}

.hint {
  display: block;
  font-size: 0.85rem;
  color: #999;
}

.uploading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.spinner {
  width: 24px;
  height: 24px;
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

.file-summary {
  margin-top: 12px;
  padding: 8px 12px;
  background: #d4edda;
  color: #155724;
  border-radius: 6px;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .metadata-fields {
    grid-template-columns: 1fr;
  }
}
</style>