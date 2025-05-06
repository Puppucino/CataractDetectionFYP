<template>
  <nav class="navbar-ribbon">
    <div class="navbar-content">
      <router-link to="/" class="nav-logo">CataractDetect</router-link>
      <div class="nav-actions">
        <v-menu offset-y>
          <template #activator="{ props }">
            <v-btn v-bind="props" icon class="profile-btn">
              <v-icon>mdi-account-circle</v-icon>
            </v-btn>
          </template>
          <v-list>
            <template v-if="isLoggedIn">
              <v-list-item>
                <router-link to="/profile" class="profile-name" style="text-decoration:none;">
                  <v-list-item-title class="profile-name">{{ userFirstName }}</v-list-item-title>
                </router-link>
              </v-list-item>
              <v-list-item @click="logout">
                <v-list-item-title>Logout</v-list-item-title>
              </v-list-item>
            </template>
            <template v-else>
              <v-list-item @click="goToLogin">
                <v-list-item-title>Login</v-list-item-title>
              </v-list-item>
            </template>
          </v-list>
        </v-menu>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuth } from '../composables/useAuth'
import { useRouter } from 'vue-router'
import { ref, watchEffect } from 'vue'
const { isLoggedIn, logout } = useAuth()
const router = useRouter()
const userFirstName = ref('')
const userLastName = ref('')

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
  if (isLoggedIn.value) {
    fetchUserProfile()
  } else {
    userFirstName.value = ''
    userLastName.value = ''
  }
  console.log('userFirstName:', userFirstName.value)
})

const goToLogin = () => {
  router.push('/login')
}
</script>

<style scoped>
.navbar-ribbon {
  width: 100%;
  background: #1976d2;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  position: static;
  top: 0;
  left: 0;
  z-index: 1000;
}
.navbar-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  padding: 0 2.5rem;
}
.nav-logo {
  font-size: 1.7rem;
  font-weight: bold;
  color: #fff;
  text-decoration: none;
  letter-spacing: 1px;
}
.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.profile-btn {
  color: #fff;
  background: none;
  box-shadow: none;
}
.profile-name {
  font-weight: bold;
  color: #1976d2;
}
</style> 