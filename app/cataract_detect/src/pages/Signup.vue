<template>
  <div class="signup-bg">
    <div class="signup-card-wrapper">
      <div class="signup-card">
        <h2>Create Your Account</h2>
        <SignupForm />
      </div>
    </div>
    <div class="login-prompt">
      <span>Already have an account?</span>
      <router-link to="/login" class="login-btn">Log in</router-link>
    </div>
  </div>
</template>

<script setup>
import SignupForm from '../components/SignupForm.vue'
</script>

<style scoped>
.signup-bg {
  min-height: 100vh;
  background: #0a4d6e;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.signup-card-wrapper {
  width: 100%;
  max-width: 430px;
  display: flex;
  flex-direction: column;
}
.signup-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 32px rgba(0,0,0,0.10);
  padding: 2.5rem 2rem 2rem 2rem;
  width: 100%;
  text-align: left;
}
.signup-card h2 {
  margin-bottom: 2rem;
  font-size: 2rem;
  font-weight: 700;
  color: #222;
}
.login-prompt {
  margin-top: 1.5rem;
  color: #fff;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  justify-content: center;
}
.login-btn {
  color: #ffd600;
  font-weight: bold;
  text-decoration: underline;
  transition: color 0.2s;
}
.login-btn:hover {
  color: #fff176;
}
</style> 