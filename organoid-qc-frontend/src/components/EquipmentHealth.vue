<template>
  <div class="equipment-section">
    <h3>🔧 Equipment Health</h3>
    
    <div v-if="!health || health.status === 'no_data'" class="info">
      No equipment data yet
    </div>
    
    <div v-else class="health-card">
      <!-- Handle both single microscope and multiple -->
      <div v-for="(data, microId) in health" :key="microId" class="micro-block">
        <div class="metric">
          <span class="label">Microscope</span>
          <span class="value">{{ microId }}</span>
        </div>
        
        <div class="metric">
          <span class="label">Images</span>
          <span class="value">{{ data.total_images }}</span>
        </div>
        
        <div class="metric">
          <span class="label">Focus Trend</span>
          <span class="value" :class="data.focus_trend < -5 ? 'warning' : 'good'">
            {{ data.focus_trend > 0 ? "+" : "" }}{{ data.focus_trend ? data.focus_trend.toFixed(2) : "N/A" }}
          </span>
        </div>
        
        <div v-if="data.issues" class="issues">
          <span v-for="(issue, idx) in data.issues" :key="idx" class="issue-item">
            {{ issue }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  health: {
    type: Object,
    default: null
  }
});
</script>

<style scoped>
.equipment-section {
  background: #f0f4f8;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  border-left: 4px solid #ff9800;
}

.equipment-section h3 {
  margin-top: 0;
  color: #333;
}

.health-card {
  background: white;
  padding: 16px;
  border-radius: 8px;
  border-left: 3px solid #ff9800;
}

.micro-block {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e0e0e0;
}

.micro-block:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.metric {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
}

.label {
  font-weight: 600;
  color: #666;
}

.value {
  font-weight: 700;
  color: #0066cc;
}

.value.warning {
  color: #ff6b6b;
}

.value.good {
  color: #28a745;
}

.issues {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.issue-item {
  padding: 4px 8px;
  background: #fff3cd;
  color: #856404;
  border-radius: 4px;
  font-size: 0.85rem;
}

.info {
  color: #999;
  font-style: italic;
  padding: 12px;
  background: white;
  border-radius: 6px;
}
</style>