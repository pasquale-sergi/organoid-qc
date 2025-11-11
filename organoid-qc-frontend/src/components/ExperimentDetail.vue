<script setup>
import { ref } from "vue";
import { useExperiments } from "../composables/useExperiments";
import UploadSection from "./UploadSection.vue";
import ThresholdControls from "./ThresholdControls.vue";
import BatchReport from "./BatchReport.vue";
import ImagesTable from "./ImagesTable.vue";
import ActionButtons from "./ActionButtons.vue";

const activeTab = ref("upload");

const props = defineProps({
  experiment: { type: Object, required: true },
  batchReport: { type: Object, default: null },
  images: { type: Array, required: true }
});

const emit = defineEmits(["update-batch-report", "update-images", "delete"]);

const {
  uploadImages,
  loadBatchReport,
  loadImages,
  deleteExperiment: deleteExp,
  exportMlReady,
  downloadScript,
  exportFull,
  batchReport: composableBatchReport,
  images: composableImages
} = useExperiments();

const uploading = ref(false);
const thresholds = ref({
  focus: 150,
  contrast: 20,
  exposure_min: 30,
  exposure_max: 225
});

const handleUpload = async (files, metadata) => {
  uploading.value = true;
  try {
    await uploadImages(props.experiment.id, files, metadata);
    await updateThresholds({ ...thresholds.value });
  } catch (e) {
    alert("Error uploading images: " + e.message);
  } finally {
    uploading.value = false;
  }
};

const updateThresholds = async (newThresholds) => {
  Object.assign(thresholds.value, newThresholds);
  try {
    await loadBatchReport(props.experiment.id, thresholds.value);
    await loadImages(props.experiment.id);
    
    // Emit the values from composable
    emit("update-batch-report", composableBatchReport.value);
    emit("update-images", composableImages.value);
  } catch (e) {
    console.error("Error updating thresholds:", e);
  }
};

const downloadFile = (content, filename, mimeType) => {
  const element = document.createElement("a");
  element.setAttribute(
    "href",
    "data:" + mimeType + ";charset=utf-8," + encodeURIComponent(content)
  );
  element.setAttribute("download", filename);
  element.style.display = "none";
  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
};

const handleExportMlReady = async () => {
  try {
    const data = await exportMlReady(props.experiment.id);
    downloadFile(data.csv, data.filename, "text/csv");
  } catch (e) {
    alert("Error exporting ML-ready images");
  }
};

const handleDownloadScript = async () => {
  try {
    const data = await downloadScript(props.experiment.id, thresholds.value);
    downloadFile(data.script, data.filename, "text/plain");
    alert(
      `✓ Script downloaded!\n\nML-Ready: ${data.ml_ready_count}/${data.total_count}\n\nInstructions:\n1. Save the script\n2. Run: python3 ${data.filename}\n3. Enter your images directory path\n4. Images will be copied to ml_ready_images/`
    );
  } catch (e) {
    console.error("❌ Error generating script:", e);
    alert("Error generating script");
  }
};

const handleExportFull = async () => {
  try {
    const data = await exportFull(props.experiment.id);
    downloadFile(data.csv, data.filename, "text/csv");
  } catch (e) {
    alert("Error exporting all images");
  }
};

const handleDelete = async () => {
  try {
    await deleteExp(props.experiment.id);
    emit("delete");
  } catch (e) {
    alert("Error deleting experiment");
  }
};
</script>

<template>
  <section class="card experiment-detail">
    <h2>{{ experiment.name }}</h2>

    <div class="tabs">
      <button 
        @click="activeTab = 'upload'"
        :class="{ active: activeTab === 'upload' }"
      >
        📤 Upload
      </button>

    </div>

    <div v-if="activeTab === 'upload'">
      <UploadSection :uploading="uploading" @upload="handleUpload" />
      <ThresholdControls :thresholds="thresholds" @update="updateThresholds" />
      <BatchReport :report="batchReport" />
      <ImagesTable :images="images" :thresholds="thresholds" />
      <ActionButtons
        :ml-ready-count="batchReport?.ml_ready_images || 0"
        @export-ml-ready="handleExportMlReady"
        @download-script="handleDownloadScript"
        @export-all="handleExportFull"
        @delete="handleDelete"
      />
    </div>

  </section>
</template>

<style scoped>
.experiment-detail {
  display: flex;
  flex-direction: column;
}

.tabs {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  border-bottom: 2px solid #e0e0e0;
}

.tabs button {
  padding: 12px 20px;
  background: none;
  border: none;
  border-bottom: 3px solid transparent;
  cursor: pointer;
  font-weight: 600;
  color: #666;
  transition: all 0.2s;
}

.tabs button.active {
  color: #0066cc;
  border-bottom-color: #0066cc;
}

.tabs button:hover {
  color: #0066cc;
}
</style>