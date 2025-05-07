import { ref } from 'vue'
import { useRouter } from 'vue-router'

export function useImageUpload() {
  const result = ref(null)
  const error = ref('')
  const loading = ref(false)
  const router = useRouter()

  const uploadImage = async (file) => {
    error.value = ''
    result.value = null
    loading.value = true
    try {
      const formData = new FormData()
      formData.append('image', file)
      const token = localStorage.getItem('token')
      const res = await fetch('https://cataract-backend-163662192726.us-central1.run.app/api/images/upload', {
        method: 'POST',
        headers: token ? { 'Authorization': `Bearer ${token}` } : {},
        body: formData
      })
      if (res.status === 401) {
        localStorage.removeItem('token')
        router.push('/')
        return
      }
      const data = await res.json()
      if (res.ok) {
        result.value = data
      } else {
        error.value = data.message || 'Upload failed'
      }
    } catch (err) {
      error.value = 'Network error'
    } finally {
      loading.value = false
    }
  }

  return { uploadImage, result, error, loading }
} 