import { ref } from 'vue'

export function useMedicalQA() {
  const answer = ref('')
  const sources = ref([])
  const loading = ref(false)
  const error = ref('')

  const askMedicalQuestion = async (question) => {
    answer.value = ''
    sources.value = []
    error.value = ''
    loading.value = true
    try {
      const res = await fetch('http://localhost:8000/api/medical/qa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      })
      const data = await res.json()
      if (res.ok) {
        answer.value = data.answer
        sources.value = data.sources
      } else {
        error.value = data.detail || 'Failed to get answer'
      }
    } catch (e) {
      error.value = 'Network error'
    } finally {
      loading.value = false
    }
  }

  return { askMedicalQuestion, answer, sources, loading, error }
} 