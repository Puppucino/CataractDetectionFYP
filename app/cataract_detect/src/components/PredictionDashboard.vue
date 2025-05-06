<template>
  <div class="dashboard-card">
    <h3>Prediction Dashboard</h3>
    <div class="dashboard-row">
      <span class="dashboard-label">Confidence
        <span class="info-icon" title="Confidence is a value between 0 and 1. Closer to 1 means more likely cataract, closer to 0 means more likely healthy.">?</span>
      </span>
      <span class="dashboard-value">{{ confidenceDisplay }}</span>
    </div>
    <div class="dashboard-row">
      <span class="dashboard-label">Severity
        <span class="info-icon" title="Severity is interpreted from the confidence score. Closer to 1 means more severe cataract, closer to 0 means healthy.">?</span>
      </span>
      <span class="dashboard-value">{{ severity }}</span>
    </div>
    <div class="dashboard-row">
      <span class="dashboard-label">Recommendation</span>
      <span class="dashboard-value dashboard-recommendation">{{ recommendation }}</span>
    </div>
    <div class="dashboard-explanation">
      <strong>How to interpret:</strong>
      <ul>
        <li><b>Confidence</b>: Value between 0 and 1. Closer to 1 = more likely cataract, closer to 0 = more likely healthy.</li>
        <li><b>Severity</b>: High severity means the model is confident about cataract; low means likely healthy.</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  prediction: String
})

// Extract confidence from prediction string
const confidence = computed(() => {
  const match = props.prediction.match(/([0-9]\.[0-9]{2})/)
  return match ? parseFloat(match[1]) : null
})

const confidenceDisplay = computed(() => {
  return confidence.value !== null ? confidence.value.toFixed(2) : 'N/A'
})

const severity = computed(() => {
  if (confidence.value === null) return 'N/A'
  if (confidence.value >= 0.8) return 'High'
  if (confidence.value >= 0.5) return 'Moderate'
  return 'Low'
})

const recommendation = computed(() => {
  if (confidence.value === null) return 'N/A'
  if (confidence.value >= 0.8) return 'Consult an ophthalmologist as soon as possible.'
  if (confidence.value >= 0.5) return 'Monitor your eye health and consider a professional checkup.'
  return 'No cataract detected. Maintain regular eye exams.'
})
</script>

<style scoped>
.dashboard-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  padding: 1.5rem 2rem;
  margin: 1.5rem 0 0 0;
  max-width: 400px;
}
.dashboard-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.7rem;
  font-size: 1.08rem;
}
.dashboard-label {
  font-weight: 500;
  color: #1976d2;
}
.dashboard-value {
  font-weight: bold;
  color: #333;
}
.info-icon {
  display: inline-block;
  margin-left: 0.4em;
  background: #e3f2fd;
  color: #1976d2;
  border-radius: 50%;
  width: 1.1em;
  height: 1.1em;
  text-align: center;
  font-size: 0.9em;
  cursor: pointer;
  border: 1px solid #1976d2;
}
.dashboard-explanation {
  margin-top: 1.2rem;
  font-size: 0.98rem;
  color: #444;
  background: #f0f7ff;
  border-radius: 8px;
  padding: 0.7rem 1rem;
}
.dashboard-recommendation {
  text-align: right;
  display: block;
  width: 100%;
}
</style> 