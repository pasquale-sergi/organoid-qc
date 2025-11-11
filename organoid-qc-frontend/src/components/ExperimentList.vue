<template>
  <section class="card experiment-list">
    <h2>📊 Experiments</h2>

    <div class="create-form">
      <input
        v-model="newName"
        type="text"
        placeholder="Enter experiment name"
        @keyup.enter="handleCreate"
      />
      <button @click="handleCreate" class="btn-primary">Create</button>
    </div>

    <div v-if="!experiments.length" class="empty-state">
      <p>No experiments yet. Create one to get started!</p>
    </div>

    <div v-else class="experiments">
      <div
        v-for="exp in experiments"
        :key="exp.id"
        class="experiment-card"
        :class="{ active: isSelected(exp.id) }"
        @click="$emit('select', exp.id)"
      >
        <div class="exp-header">
          <strong>{{ exp.name }}</strong>
          <span class="exp-date">{{ formatDate(exp.created_at) }}</span>
        </div>
        <button class="btn-view" @click.stop="$emit('select', exp.id)">
          View Details →
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  experiments: {
    type: Array,
    required: true
  },
  selectedExpId: {
    type: Number,
    default: null
  }
});

const emit = defineEmits(["create", "select"]);
const newName = ref("");

const handleCreate = () => {
  if (!newName.value.trim()) return;
  emit("create", newName.value);
  newName.value = "";
};
const isSelected = (expId) => expId === props.selectedExpId;

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric"
  });
};
</script>

<style scoped>
.experiment-list {
  display: flex;
  flex-direction: column;
  height: fit-content;
  position: sticky;
  top: 20px;
}

.create-form {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.create-form input {
  flex: 1;
}

.create-form button {
  min-width: 100px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
  font-style: italic;
}

.experiments {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 600px;
  overflow-y: auto;
}

.experiment-card {
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
}

.experiment-card:hover {
  border-color: #0066cc;
  background: #f8f9fa;
}

.experiment-card.active {
  border-color: #0066cc;
  background: #e7f0ff;
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.exp-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.exp-header strong {
  color: #333;
}

.exp-date {
  font-size: 0.8rem;
  color: #999;
}

.btn-view {
  width: 100%;
  background: #0066cc;
  color: white;
  padding: 8px;
  font-size: 0.9rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-view:hover {
  background: #004499;
}
</style>