<template>
  <div class="login-bg">
    <div class="login-card">
      <h2>Login to Your Account</h2>
      <LoginForm />
    </div>
    <div class="signup-prompt">
      <span>Don't have an account?</span>
      <router-link to="/signup" class="signup-btn">Sign up</router-link>
    </div>
  </div>
</template>

<script setup>
import LoginForm from '../components/LoginForm.vue'
</script>

<style scoped>
.login-bg {
  min-height: 100vh;
  background: #0a4d6e;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.login-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 32px rgba(0,0,0,0.10);
  padding: 2.5rem 2rem 2rem 2rem;
  max-width: 400px;
  width: 100%;
  text-align: left;
}
.login-card h2 {
  margin-bottom: 2rem;
  font-size: 2rem;
  font-weight: 700;
  color: #222;
}
.signup-prompt {
  margin-top: 1.5rem;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  justify-content: center;
}
.signup-btn {
  color: #ffd600;
  font-weight: bold;
  text-decoration: underline;
  transition: color 0.2s;
}
.signup-btn:hover {
  color: #fff176;
}
</style> 