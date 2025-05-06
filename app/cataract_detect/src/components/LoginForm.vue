<template>
  <form class="login-form" @submit.prevent="onSubmit">
    <div class="form-group">
      <label for="email">Email</label>
      <input v-model="email" type="email" id="email" required />
    </div>
    <div class="form-group">
      <label for="password">Password</label>
      <input v-model="password" type="password" id="password" required />
    </div>
    <button type="submit" class="btn">Login</button>
    <p v-if="error" class="error">{{ error }}</p>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../composables/useAuth'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const { login } = useAuth()

const onSubmit = async () => {
  error.value = ''
  const result = await login(email.value, password.value)
  if (!result.success) {
    error.value = result.message
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.5rem;
}
label {
  font-weight: 500;
  color: #222;
}
input {
  width: 100%;
  padding: 0.9rem 1rem;
  border: 1.5px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1.1rem;
  background: #f8fafc;
  transition: box-shadow 0.2s, border 0.2s;
}
input:focus {
  outline: none;
  border: 1.5px solid #1abc9c;
  box-shadow: 0 0 0 2px #1abc9c22;
}
.btn {
  background: #1976d2;
  color: #fff;
  border: none;
  padding: 1rem 0;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: background 0.2s;
}
.btn:hover {
  background: #1565c0;
}
.error {
  color: #d32f2f;
  margin-top: 0.5rem;
  font-size: 1rem;
}
</style> 