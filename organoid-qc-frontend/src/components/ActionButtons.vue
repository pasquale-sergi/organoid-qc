<template>
  <div class="actions">
    <button
      v-if="mlReadyCount > 0"
      @click="$emit('export-ml-ready')"
      class="btn-primary"
    >
      📥 Export ML-Ready (CSV)
    </button>
    <button
      v-if="mlReadyCount > 0"
      @click="$emit('download-script')"
      class="btn-info"
    >
      💾 Download Organize Script
    </button>
    <button @click="$emit('export-all')" class="btn-secondary">
      📥 Export All
    </button>
    <button @click="handleDelete" class="btn-danger">
      🗑️ Delete Experiment
    </button>
  </div>
</template>

<script setup>
defineProps({
  mlReadyCount: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(["export-ml-ready", "download-script", "export-all", "delete"]);

const handleDelete = () => {
  if (confirm("Are you sure? This will delete all images and data for this experiment.")) {
    emit("delete");
  }
};
</script>

<style scoped>
.actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
  flex-wrap: wrap;
}

.actions button {
  flex: 1;
  min-width: 160px;
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn-primary {
  background: #0066cc;
  color: white;
}

.btn-primary:hover {
  background: #004499;
  box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.btn-info {
  background: #17a2b8;
  color: white;
}

.btn-info:hover {
  background: #138496;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-secondary:hover {
  background: #5a6268;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn-danger:hover {
  background: #c82333;
  box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
}

@media (max-width: 768px) {
  .actions {
    flex-direction: column;
  }

  .actions button {
    width: 100%;
  }
}
</style>