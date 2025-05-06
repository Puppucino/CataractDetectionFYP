<template>
  <v-container class="profile-page" fluid>
    <v-row>
      <v-col cols="12">
        <v-btn color="primary" class="mb-4" @click="goToChat">Go to Chat</v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Edit Profile</v-card-title>
          <v-card-text>
            <v-form ref="profileForm" v-model="profileValid" @submit.prevent="updateProfile">
              <v-text-field v-model="profile.first_name" label="First Name" :rules="[v => !!v || 'Required']" required />
              <v-text-field v-model="profile.last_name" label="Last Name" :rules="[v => !!v || 'Required']" required />
              <v-text-field v-model="profile.email" label="Email" :rules="[v => !!v || 'Required']" required />
              <v-text-field v-model="profile.phone" label="Phone" />
              <v-btn type="submit" color="primary" :loading="profileLoading">Save</v-btn>
            </v-form>
            <v-alert v-if="profileMsg" :type="profileMsgType" class="mt-2">{{ profileMsg }}</v-alert>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Change Password</v-card-title>
          <v-card-text>
            <v-form ref="passwordForm" v-model="passwordValid" @submit.prevent="changePassword">
              <v-text-field v-model="password.old_password" label="Old Password" type="password" :rules="[v => !!v || 'Required']" required />
              <v-text-field v-model="password.new_password" label="New Password" type="password" :rules="[v => !!v || 'Required']" required />
              <v-text-field v-model="password.confirm_new_password" label="Confirm New Password" type="password" :rules="[v => v === password.new_password || 'Passwords do not match']" required />
              <v-btn type="submit" color="primary" :loading="passwordLoading">Change</v-btn>
            </v-form>
            <v-alert v-if="passwordMsg" :type="passwordMsgType" class="mt-2">{{ passwordMsg }}</v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title>Detection History</v-card-title>
          <v-card-text>
            <v-data-table :headers="historyHeaders" :items="history" class="elevation-1">
              <template #item.image="{ item }">
                <img :src="`http://localhost:8000/uploads/${item.filename}`" alt="uploaded" style="height:48px;max-width:64px;object-fit:cover;border-radius:4px;" />
              </template>
              <template #item.created_at="{ item }">
                {{ formatDate(item.created_at) }}
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
const profile = ref({ first_name: '', last_name: '', email: '', phone: '' })
const profileValid = ref(false)
const profileLoading = ref(false)
const profileMsg = ref('')
const profileMsgType = ref('success')
const password = ref({ old_password: '', new_password: '', confirm_new_password: '' })
const passwordValid = ref(false)
const passwordLoading = ref(false)
const passwordMsg = ref('')
const passwordMsgType = ref('success')
const history = ref([])
const historyHeaders = [
  { text: 'Image', value: 'image', sortable: false },
  { text: 'Filename', value: 'filename' },
  { text: 'Prediction', value: 'prediction' },
  { text: 'Date', value: 'created_at' }
]

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleString()
}

async function fetchProfile() {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/')
    return
  }
  const res = await fetch('http://localhost:8000/api/auth/me', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  if (res.status === 401) {
    localStorage.removeItem('token')
    router.push('/')
    return
  }
  const data = await res.json()
  profile.value = { ...profile.value, ...data }
  if (data.phone) profile.value.phone = data.phone
}

async function updateProfile() {
  profileLoading.value = true
  profileMsg.value = ''
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/api/auth/profile', {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(profile.value)
  })
  const data = await res.json()
  profileLoading.value = false
  if (res.ok && data.success) {
    profileMsg.value = 'Profile updated successfully.'
    profileMsgType.value = 'success'
  } else {
    profileMsg.value = data.detail || 'Failed to update profile.'
    profileMsgType.value = 'error'
  }
}

async function changePassword() {
  passwordLoading.value = true
  passwordMsg.value = ''
  if (password.value.new_password !== password.value.confirm_new_password) {
    passwordMsg.value = 'New passwords do not match.'
    passwordMsgType.value = 'error'
    passwordLoading.value = false
    return
  }
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/api/auth/password', {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ old_password: password.value.old_password, new_password: password.value.new_password })
  })
  const data = await res.json()
  passwordLoading.value = false
  if (res.ok && data.success) {
    passwordMsg.value = 'Password changed successfully.'
    passwordMsgType.value = 'success'
    password.value.old_password = ''
    password.value.new_password = ''
    password.value.confirm_new_password = ''
  } else {
    passwordMsg.value = data.detail || 'Failed to change password.'
    passwordMsgType.value = 'error'
  }
}

async function fetchHistory() {
  const token = localStorage.getItem('token')
  const res = await fetch('http://localhost:8000/api/images/history', {
    headers: { 'Authorization': `Bearer ${token}` }
  })
  if (res.ok) {
    history.value = await res.json()
  }
}

function goToChat() {
  router.push('/upload')
}

onMounted(() => {
  fetchProfile()
  fetchHistory()
})
</script>

<style scoped>
.profile-page {
  margin-top: 32px;
}
</style> 