<template>
  <div v-if="report" class="batch-report">
    <h3>📈 Batch Quality Report</h3>

    <div class="metrics-grid">
      <div class="metric-card">
        <span class="metric-label">Total Images</span>
        <span class="metric-value">{{ report.total_images }}</span>
      </div>
      <div class="metric-card success">
        <span class="metric-label">ML Ready</span>
        <span class="metric-value">{{ report.ml_ready_images }}</span>
      </div>
      <div class="metric-card success">
        <span class="metric-label">Pass Rate</span>
        <span class="metric-value">{{ report.pass_rate }}%</span>
      </div>
      <div class="metric-card">
        <span class="metric-label">Avg Focus</span>
        <span class="metric-value">{{ report.avg_focus?.toFixed(0) || "—" }}</span>
      </div>
      <div class="metric-card">
        <span class="metric-label">Avg Contrast</span>
        <span class="metric-value">{{ report.avg_contrast?.toFixed(1) || "—" }}</span>
      </div>
      <div class="metric-card">
        <span class="metric-label">Avg Exposure</span>
        <span class="metric-value">{{ report.avg_exposure?.toFixed(0) || "—" }}</span>
      </div>
    </div>

    <!-- Sessions Breakdown -->
    <div v-if="report.sessions" class="sessions-section">
      <h4>Imaging Sessions</h4>
      <div
        v-for="(session, sessionId) in report.sessions"
        :key="sessionId"
        class="session-card"
      >
        <div class="session-header">
          <strong>{{ sessionId || "Unknown" }}</strong>
          <span class="session-stat">
            {{ session.ready }}/{{ session.total }} ready
            ({{ Math.round((session.ready / session.total) * 100) }}%)
          </span>
        </div>
        <div v-if="session.issues.length" class="session-issues">
          <span
            v-for="(issue, idx) in session.issues.slice(0, 3)"
            :key="idx"
            class="issue-tag"
          >
            ⚠️ {{ issue }}
          </span>
          <span v-if="session.issues.length > 3" class="issue-more">
            +{{ session.issues.length - 3 }} more issues
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  report: {
    type: Object,
    default: null
  }
});
</script>

<style scoped>
.batch-report {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  border-left: 4px solid #0066cc;
}

.batch-report h3 {
  margin-top: 0;
  margin-bottom: 16px;
  color: #333;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.metric-card {
  background: white;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #0066cc;
  text-align: center;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.metric-card.success {
  border-left-color: #28a745;
}

.metric-card.success .metric-value {
  color: #28a745;
}

.metric-label {
  display: block;
  font-size: 0.8rem;
  color: #666;
  margin-bottom: 8px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-value {
  display: block;
  font-size: 1.5rem;
  font-weight: 700;
  color: #0066cc;
}

.sessions-section {
  margin-top: 24px;
}

.sessions-section h4 {
  margin: 0 0 12px 0;
  color: #333;
  font-size: 1rem;
}

.session-card {
  background: white;
  padding: 12px;
  border-radius: 6px;
  margin-bottom: 8px;
  border-left: 3px solid #0066cc;
}

.session-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.session-header strong {
  color: #333;
}

.session-stat {
  background: #e7f0ff;
  color: #0066cc;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 500;
}

.session-issues {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.issue-tag {
  background: #fff3cd;
  color: #856404;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}

.issue-more {
  background: #e2e3e5;
  color: #333;
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
}
</style>