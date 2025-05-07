import { ref } from 'vue'

const isLoggedIn = ref(!!localStorage.getItem('token'))

export function useAuth() {
  const login = async (email, password) => {
    try {
      const res = await fetch('https://cataract-backend-163662192726.us-central1.run.app/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      const data = await res.json()
      if (res.ok && data.token) {
        localStorage.setItem('token', data.token)
        if (data.first_name) localStorage.setItem('first_name', data.first_name)
        if (data.last_name) localStorage.setItem('last_name', data.last_name)
        isLoggedIn.value = true
        return { success: true }
      } else {
        return { success: false, message: data.message || 'Login failed' }
      }
    } catch (err) {
      return { success: false, message: 'Network error' }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    isLoggedIn.value = false
  }

  return { isLoggedIn, login, logout }
} 