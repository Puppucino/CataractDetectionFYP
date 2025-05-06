<template>
  <div class="upload-page">
    <v-container>
      <v-row justify="center">
        <v-col cols="12" md="8">
          <section class="upload-section">
            <h2>Upload Eye Image for Cataract Detection</h2>
            <ImageUploader />
          </section>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script setup>
import ImageUploader from '../components/ImageUploader.vue'
</script>

<style scoped>
.upload-page {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.upload-section {
  margin-top: 2rem;
  width: 100%;
  background: #f9f9f9;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
</style> 