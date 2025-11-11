<template>
  <div class="app">
    <header class="app-header">
      <h1>🧬 OrganoidQC</h1>
      <p>Image Quality Control for Organoid Screening</p>
    </header>

    <div class="app-content">
      <ExperimentList
        :experiments="experiments"
        :selected-exp-id="selectedExp?.id"
        @create="createExperiment"
        @select="selectExperiment"
      />

      <ExperimentDetail
        v-if="selectedExp"
        :experiment="selectedExp"
        :batch-report="batchReport"
        :images="images"
        @update-batch-report="(report) => (batchReport = report)"
        @update-images="(imgs) => (images = imgs)"
        @delete="() => deleteExperiment(selectedExp.id)" 
      />

      <div v-else class="empty-state">
        <p>Select an experiment to get started</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useExperiments } from "./composables/useExperiments";
import ExperimentList from "./components/ExperimentList.vue";
import ExperimentDetail from "./components/ExperimentDetail.vue";

const {
  experiments,
  selectedExp,
  batchReport,
  images,
  loadExperiments,
  createExperiment: createExp,
  selectExperiment,
  deleteExperiment
} = useExperiments();

onMounted(() => loadExperiments());

const createExperiment = async (name) => {
  if (await createExp(name)) {
    await loadExperiments();
  }
};


</script>

<style scoped>
:root {
  --primary: #0066cc;
  --primary-dark: #004499;
  --success: #28a745;
  --danger: #dc3545;
  --light: #f8f9fa;
  --dark: #1a1a1a;
  --border: #e0e0e0;
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.12);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background: var(--light);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.app-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  padding: 40px 20px;
  text-align: center;
  box-shadow: var(--shadow-md);
}

.app-header h1 {
  font-size: 2.5rem;
  margin-bottom: 8px;
}

.app-header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.app-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 20px;
  padding: 20px;
  max-width: 1600px;
  margin: 0 auto;
  width: 100%;
  flex: 1;
}

.empty-state {
  background: white;
  padding: 60px 20px;
  border-radius: 12px;
  text-align: center;
  color: #999;
  font-style: italic;
}

@media (max-width: 1024px) {
  .app-content {
    grid-template-columns: 1fr;
  }
}
</style>