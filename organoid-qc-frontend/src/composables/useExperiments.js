import { ref } from "vue";
import { useApi } from "./useApi";

export function useExperiments() {
  const { get, post, del, isLoading, apiError } = useApi();

  const experiments = ref([]);
  const selectedExp = ref(null);
  const batchReport = ref(null);
  const images = ref([]);

  const loadExperiments = async () => {
    try {
      const data = await get("/experiments");
      experiments.value = data;
    } catch (e) {
      console.error("Failed to load experiments", e);
    }
  };

  const createExperiment = async (name) => {
    try {
      await post("/experiments", { name });
      await loadExperiments();
      return true;
    } catch (e) {
      console.error("Failed to create experiment", e);
      return false;
    }
  };

  const selectExperiment = async (expId) => {
    selectedExp.value = experiments.value.find((e) => e.id === expId);
    await loadBatchReport(expId);
    await loadImages(expId);
  };

  const loadBatchReport = async (expId, thresholds = {}) => {
    try {
      const params = new URLSearchParams({
        focus_threshold: thresholds.focus || 80,
        contrast_threshold: thresholds.contrast || 20,
        exposure_min: thresholds.exposure_min || 30,
        exposure_max: thresholds.exposure_max || 225
      });
      const data = await get(
        `/experiments/${expId}/batch-report?${params.toString()}`
      );
      batchReport.value = data;
    } catch (e) {
      console.error("Failed to load batch report", e);
    }
  };

  const loadImages = async (expId) => {
    try {
      const data = await get(`/experiments/${expId}/images`);
      images.value = data;
    } catch (e) {
      console.error("Failed to load images", e);
    }
  };

  const uploadImages = async (expId, files, metadata) => {
    try {
      const { uploadFile } = useApi();
      
      for (let file of files) {
        await uploadFile(
          `/upload/${expId}`,
          file,
          {
            imaging_session_id: metadata.session,
            microscope_id: metadata.microscope,
            operator_id: metadata.operator
          }
        );
      }
      
      await loadBatchReport(expId);
      await loadImages(expId);
      return true;
    } catch (e) {
      console.error("Failed to upload images", e);
      return false;
    }
  };

  const deleteExperiment = async (expId) => {
    try {
      await del(`/experiments/${expId}`);
      await loadExperiments();
      selectedExp.value = null;
      batchReport.value = null;
      images.value = [];
      return true;
    } catch (e) {
      console.error("Failed to delete experiment", e);
      return false;
    }
  };

  const exportMlReady = async (expId) => {
    try {
      return await get(`/experiments/${expId}/export-ml-ready`);
    } catch (e) {
      console.error("Failed to export ML-ready", e);
      throw e;
    }
  };

  const downloadScript = async (expId, thresholds) => {
    try {
      const params = new URLSearchParams({
        focus_threshold: thresholds.focus,
        contrast_threshold: thresholds.contrast,
        exposure_min: thresholds.exposure_min,
        exposure_max: thresholds.exposure_max
      });
      return await get(
        `/experiments/${expId}/generate-copy-script?${params.toString()}`
      );
    } catch (e) {
      console.error("Failed to generate script", e);
      throw e;
    }
  };

  const exportFull = async (expId) => {
    try {
      return await get(`/experiments/${expId}/export`);
    } catch (e) {
      console.error("Failed to export all", e);
      throw e;
    }
  };

  return {
    // State
    experiments,
    selectedExp,
    batchReport,
    images,
    isLoading,
    apiError,

    // Methods
    loadExperiments,
    createExperiment,
    selectExperiment,
    loadBatchReport,
    loadImages,
    uploadImages,
    deleteExperiment,
    exportMlReady,
    downloadScript,
    exportFull
  };
}