<template>
  <form class="signup-form" @submit.prevent="onSubmit">
    <div class="form-row">
      <div class="form-group">
        <label for="firstName">First name</label>
        <input v-model="firstName" type="text" id="firstName" required />
      </div>
      <div class="form-group">
        <label for="lastName">Last name</label>
        <input v-model="lastName" type="text" id="lastName" required />
      </div>
    </div>
    <div class="form-group">
      <label for="email">Email</label>
      <input v-model="email" type="email" id="email" required />
    </div>
    <div class="form-group">
      <label for="phone">Phone number</label>
      <div class="phone-input">
        <select v-model="countryCode" required>
          <option value="+1">+1 (US)</option>
          <option value="+44">+44 (UK)</option>
          <option value="+60">+60 (MY)</option>
          <option value="+91">+91 (IN)</option>
          <!-- Add more country codes as needed -->
        </select>
        <input v-model="phone" type="tel" id="phone" required placeholder="123456789" />
      </div>
    </div>
    <div class="form-group">
      <label for="password">Password</label>
      <div class="password-input">
        <input :type="showPassword ? 'text' : 'password'" v-model="password" id="password" required />
        <button type="button" class="toggle-btn" @click="showPassword = !showPassword">
          {{ showPassword ? 'Hide' : 'Show' }}
        </button>
      </div>
    </div>
    <div class="form-group">
      <label for="confirmPassword">Confirm password</label>
      <div class="password-input">
        <input :type="showConfirmPassword ? 'text' : 'password'" v-model="confirmPassword" id="confirmPassword" required />
        <button type="button" class="toggle-btn" @click="showConfirmPassword = !showConfirmPassword">
          {{ showConfirmPassword ? 'Hide' : 'Show' }}
        </button>
      </div>
    </div>
    <button type="submit" class="btn">Sign up</button>
    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="success" class="success">{{ success }}</p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const firstName = ref('')
const lastName = ref('')
const email = ref('')
const countryCode = ref('+1')
const phone = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const success = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)

const onSubmit = async () => {
  error.value = ''
  success.value = ''
  if (!firstName.value || !lastName.value || !email.value || !phone.value || !password.value || !confirmPassword.value) {
    error.value = 'Please fill in all fields.'
    return
  }
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }
  // Send registration request to backend
  try {
    const res = await fetch('http://localhost:8000/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: firstName.value + ' ' + lastName.value,
        email: email.value,
        password: password.value,
        phone: countryCode.value + phone.value
      })
    })
    const data = await res.json()
    if (res.ok) {
      success.value = 'Registration successful! Redirecting to login...'
      setTimeout(() => router.push('/login'), 1000)
    } else {
      error.value = data.message || 'Registration failed.'
    }
  } catch (err) {
    error.value = 'Network error.'
  }
}
</script>

<style scoped>
.signup-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.form-row {
  display: flex;
  gap: 1rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
  flex: 1;
}
label {
  font-weight: 500;
  color: #222;
}
input, select {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1.1rem;
  background: #f8fafc;
  transition: box-shadow 0.2s, border 0.2s;
}
input:focus, select:focus {
  outline: none;
  border: 1.5px solid #1abc9c;
  box-shadow: 0 0 0 2px #1abc9c22;
}
.phone-input {
  display: flex;
  gap: 0.5rem;
  width: 100%;
}
.password-input {
  display: flex;
  align-items: center;
  width: 100%;
}
.toggle-btn {
  background: none;
  border: none;
  color: #1976d2;
  font-weight: bold;
  margin-left: 0.5rem;
  cursor: pointer;
  font-size: 1rem;
  padding: 0 0.5rem;
}
.btn {
  background: #ffd600;
  color: #222;
  border: none;
  padding: 1rem 0;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
.btn:hover {
  background: #ffe066;
}
.error {
  color: #d32f2f;
  margin-top: 0.5rem;
  font-size: 1rem;
}
.success {
  color: #43a047;
  margin-top: 0.5rem;
  font-size: 1rem;
}
</style> 