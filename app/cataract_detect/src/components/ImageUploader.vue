<template>
  <div class="chatgpt-container wide-90">
    <div class="chatgpt-header">CataractDetect AI</div>
    <div class="chatgpt-chat-area-wrapper">
      <div class="chatgpt-chat-area" :class="{ 'blurred': !isLoggedIn }">
        <div v-for="(msg, idx) in chat" :key="idx" :class="['chatgpt-bubble', msg.role === 'user' ? 'chatgpt-user' : 'chatgpt-ai']">
          <div :class="msg.role === 'user' ? 'chatgpt-user-label' : 'chatgpt-ai-label'">
            {{ msg.role === 'user' ? userFirstName : 'AI Ophthalmologist' }}
          </div>
          <div :class="msg.role === 'user' ? 'chatgpt-user-content' : 'chatgpt-ai-content'">
            <template v-if="msg.imageUrl">
              <div class="prediction"><strong>Prediction:</strong> {{ msg.content }}</div>
              <img :src="msg.imageUrl" alt="Uploaded Eye" class="chatgpt-image" />
              <Dashboard v-if="msg.content" :prediction="msg.content" />
            </template>
            <template v-else>
              <span v-html="formatMessage(msg.content)"></span>
            </template>
          </div>
        </div>
        <div v-if="aiLoading" class="chatgpt-bubble chatgpt-ai">
          <div class="chatgpt-ai-label">AI Ophthalmologist</div>
          <div class="chatgpt-ai-content"><span class="spinner"></span> Generating explanation...</div>
        </div>
        <div v-if="hasUploaded && !aiLoading" class="faq-section">
          <div class="faq-header">Common Questions:</div>
          <div class="faq-buttons">
            <button 
              v-for="(faq, index) in faqs" 
              :key="index"
              class="faq-btn"
              @click="askFAQ(faq)"
            >
              {{ faq }}
            </button>
          </div>
        </div>
      </div>
      <div v-if="!isLoggedIn" class="login-overlay">
        <div class="login-prompt">
          <p>Please <router-link to="/login">log in</router-link> to use the chat function.</p>
        </div>
      </div>
    </div>
    <template v-if="isLoggedIn">
      <form v-if="!hasUploaded" class="chatgpt-upload-bar" @submit.prevent="onUpload">
        <input type="file" id="image" accept="image/*" @change="onFileChange" :disabled="loading" required />
        <button type="submit" class="btn" :disabled="loading">
          <span v-if="loading"><span class="spinner"></span> Uploading...</span>
          <span v-else>Upload</span>
        </button>
      </form>
      <form v-else class="chatgpt-input-bar" @submit.prevent="onAsk">
        <input v-model="userInput" type="text" placeholder="Ask anything..." :disabled="loading || aiLoading" />
        <button type="submit" class="btn" :disabled="!userInput || loading || aiLoading">
          <span v-if="aiLoading" class="spinner"></span>
          <span v-else>Send</span>
        </button>
      </form>
    </template>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watchEffect } from 'vue'
import { useImageUpload } from '../composables/useImageUpload'
import { useMedicalQA } from '../composables/useMedicalQA'
import { useAuth } from '../composables/useAuth'
import Dashboard from './PredictionDashboard.vue'

const file = ref(null)
const { uploadImage, result, error, loading } = useImageUpload()
const aiLoading = ref(false)
const userInput = ref('')
const chat = ref([])
const backendUrl = 'http://localhost:8000'

const userFirstName = ref('')
const userLastName = ref('')

const { askMedicalQuestion, answer: medicalAnswer, sources: medicalSources, loading: medicalLoading, error: medicalError } = useMedicalQA()
const { isLoggedIn } = useAuth()

const faqs = [
  "What are the treatment options for cataracts?",
  "How long does cataract surgery take?",
  "What are the early symptoms of cataracts?",
  "Can cataracts be prevented?",
  "What is the recovery time after cataract surgery?"
]

const fetchUserProfile = async () => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      const res = await fetch('http://localhost:8000/api/auth/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      if (res.ok) {
        const data = await res.json()
        userFirstName.value = data.first_name
        userLastName.value = data.last_name
      }
    } catch {}
  }
}

watchEffect(() => {
  if (localStorage.getItem('token')) {
    fetchUserProfile()
  } else {
    userFirstName.value = ''
    userLastName.value = ''
  }
})

const hasUploaded = computed(() => chat.value.some(m => m.imageUrl))

const formatMessage = (msg) => {
  if (!msg) return ''
  return msg.replace(/\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
}

onMounted(() => {
  chat.value = [
    {
      role: 'ai',
      content: `Hi ${userFirstName.value || 'User'}! Please upload an eye image for cataract detection. I will analyze it and explain the result as an AI ophthalmologist.`
    }
  ]
})

watchEffect(() => {
  if (
    chat.value.length === 1 &&
    chat.value[0].role === 'ai' &&
    chat.value[0].content.startsWith('Hi')
  ) {
    chat.value[0].content = `Hi ${userFirstName.value || 'User'}! Please upload an eye image for cataract detection. I will analyze it and explain the result as an AI ophthalmologist.`
  }
})

const onFileChange = (e) => {
  file.value = e.target.files[0]
}

const onUpload = async () => {
  if (!file.value) return
  chat.value = chat.value.filter(m => !m.imageUrl)
  await uploadImage(file.value)
  if (result.value && result.value.prediction) {
    chat.value.push({
      role: 'user',
      content: result.value.prediction,
      imageUrl: result.value.imageUrl.startsWith('http') ? result.value.imageUrl : backendUrl + result.value.imageUrl
    })
    aiLoading.value = true
    try {
      const res = await fetch('http://localhost:8000/api/deepseek/explain', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ result: result.value.prediction, lastName: userLastName.value })
      })
      const data = await res.json()
      chat.value.push({ role: 'ai', content: data.explanation })
    } catch (e) {
      chat.value.push({ role: 'ai', content: 'Failed to get explanation.' })
    } finally {
      aiLoading.value = false
    }
  }
}

const onAsk = async () => {
  if (!userInput.value.trim()) return
  const question = userInput.value.trim()
  chat.value.push({ role: 'user', content: question })
  userInput.value = ''
  aiLoading.value = true
  // Simple keyword check for medical Q&A
  const medicalKeywords = ['cataract', 'treatment', 'symptom', 'surgery', 'prevention', 'risk', 'cause', 'faq']
  const isMedicalQA = medicalKeywords.some(k => question.toLowerCase().includes(k))
  if (isMedicalQA) {
    await askMedicalQuestion(question)
    if (medicalAnswer.value) {
      let sourcesText = ''
      if (medicalSources.value.length) {
        sourcesText = '\n\nSources: ' + medicalSources.value.join(', ')
      }
      chat.value.push({ role: 'ai', content: medicalAnswer.value + sourcesText })
    } else if (medicalError.value) {
      chat.value.push({ role: 'ai', content: 'Error: ' + medicalError.value })
    }
    aiLoading.value = false
    return
  }
  try {
    const messages = chat.value.map(m => ({
      role: m.role === 'user' ? 'user' : 'assistant',
      content: m.content
    }))
    const res = await fetch('http://localhost:8000/api/deepseek/explain', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages, lastName: userLastName.value })
    })
    const data = await res.json()
    chat.value.push({ role: 'ai', content: data.explanation })
  } catch (e) {
    chat.value.push({ role: 'ai', content: 'Failed to get explanation.' })
  } finally {
    aiLoading.value = false
  }
}

const askFAQ = async (question) => {
  userInput.value = question
  await onAsk()
}
</script>

<style scoped>
.chatgpt-container.wide-90 {
  max-width: 50vw;
}
.chatgpt-container {
  max-width: 600px;
  margin: 2.5rem auto 0 auto;
  display: flex;
  flex-direction: column;
  background: #f5faff;
  border-radius: 18px;
  box-shadow: 0 8px 48px rgba(0,0,0,0.18);
  min-height: 70vh;
}
.chatgpt-header {
  background: #1976d2;
  color: #fff;
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  padding: 1.2rem 0 1rem 0;
  border-radius: 18px 18px 0 0;
  letter-spacing: 1px;
}
.chatgpt-chat-area-wrapper {
  position: relative;
}
.blurred {
  filter: blur(4px);
  pointer-events: none;
  user-select: none;
}
.login-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2;
}
.login-prompt {
  background: rgba(255,255,255,0.85);
  padding: 2rem 2.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
  font-size: 1.15rem;
  text-align: center;
}
.chatgpt-chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  padding: 2rem 2.5rem 1rem 2.5rem;
  overflow-y: auto;
}
.chatgpt-bubble {
  display: flex;
  flex-direction: column;
  max-width: 90%;
  border-radius: 16px;
  padding: 1rem 1.2rem;
  margin-bottom: 0.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.chatgpt-user {
  align-self: flex-end;
  background: #e3f2fd;
  color: #0a4d6e;
}
.chatgpt-ai {
  align-self: flex-start;
  background: #fffde7;
  color: #222;
}
.chatgpt-user-label, .chatgpt-ai-label {
  font-size: 0.95rem;
  font-weight: bold;
  margin-bottom: 0.3rem;
}
.chatgpt-user-label {
  color: #1976d2;
}
.chatgpt-ai-label {
  color: #ffd600;
}
.chatgpt-user-content, .chatgpt-ai-content {
  font-size: 1.08rem;
}
.prediction {
  margin-bottom: 0.5rem;
}
.chatgpt-image {
  margin-top: 0.5rem;
  max-width: 220px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.chatgpt-upload-bar, .chatgpt-input-bar {
  display: flex;
  gap: 1rem;
  align-items: center;
  margin: 2rem 2.5rem 2rem 2.5rem;
  padding-bottom: 0.5rem;
}
.chatgpt-upload-bar input[type="file"], .chatgpt-input-bar input[type="text"] {
  flex: 1;
  padding: 0.9rem 1.1rem;
  border-radius: 8px;
  border: 1.5px solid #e0e0e0;
  font-size: 1.08rem;
}
.btn {
  background: #1976d2;
  color: #fff;
  border: none;
  padding: 0.9rem 2rem;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.spinner {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #1976d2;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  animation: spin 1s linear infinite;
  display: inline-block;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.error {
  color: #d32f2f;
  margin-top: 0.5rem;
  text-align: center;
}
.faq-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 1.5rem 0;
  padding: 1rem;
  background: #f0f7ff;
  border-radius: 12px;
}
.faq-header {
  font-weight: bold;
  color: #1976d2;
  font-size: 1.1rem;
}
.faq-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
}
.faq-btn {
  background: #fff;
  border: 1.5px solid #1976d2;
  color: #1976d2;
  padding: 0.6rem 1rem;
  border-radius: 20px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
}
.faq-btn:hover {
  background: #1976d2;
  color: #fff;
}
</style> 