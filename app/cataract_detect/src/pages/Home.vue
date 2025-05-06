<template>
  <div>
    <div class="home-hero">
      <h1>Cataract Detection</h1>
      <p class="subtitle">
        Helps to determine whether a person has cataract or not based on symptoms and eye images.
      </p>
      <div class="hero-actions">
        <router-link to="/upload" class="btn primary">Check Yourself</router-link>
        <a href="https://www.aao.org/eye-health/diseases/what-are-cataracts" target="_blank" class="btn secondary">Learn More</a>
      </div>
    </div>
    <div class="main-content centered">
      <v-row align="center" justify="center" class="w-100">
        <v-col cols="12" md="6">
          <section class="cataract-info">
            <h2>What Are Cataracts?</h2>
            <p>
              A cataract occurs when the natural lens inside your eye becomes cloudy, making your vision blurry, hazy, or less vibrant. This cloudiness is caused by the breakdown of proteins in the lens, which can make it feel like you're looking through a foggy window. Common symptoms include blurred vision, double vision, increased sensitivity to light, trouble seeing at night, and colors appearing faded or yellowed.
            </p>
            <p>
              Cataracts most often develop as a part of the natural aging process, but they can also be influenced by factors such as family history, diabetes, eye injuries, prolonged sun exposure, certain medications, and smoking. While cataracts can gradually worsen over time, they are treatable. If vision problems begin to interfere with daily life, cataract surgery can restore clear sight by replacing the cloudy lens with an artificial one.
            </p>
            <p>
              <a href="https://www.aao.org/eye-health/diseases/what-are-cataracts" target="_blank" rel="noopener">Learn more from the American Academy of Ophthalmology</a>
            </p>
          </section>
        </v-col>
        <v-col cols="12" md="6">
          <v-carousel cycle interval="5000" show-arrows="false" hide-delimiters height="340">
            <v-carousel-item v-for="(img, i) in images" :key="i">
              <img :src="img" style="width:100%;height:340px;object-fit:cover;border-radius:8px;" />
            </v-carousel-item>
          </v-carousel>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import img1 from '../assets/pexels-pavel-danilyuk-5996602.jpg'
import img2 from '../assets/pexels-pixabay-63320.jpg'
import img3 from '../assets/pexels-karolina-grabowska-5201875.jpg'
import img4 from '../assets/pexels-shkrabaanthony-6749787.jpg'

const images = [img1, img2, img3, img4]
</script>

<style scoped>
.home-hero {
  background: #0a4d6e;
  color: #fff;
  text-align: center;
  padding: 3rem 1rem 2rem 1rem;
  border-radius: 0 0 32px 32px;
}
.home-hero h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}
.subtitle {
  font-size: 1.2rem;
  margin-bottom: 1.5rem;
}
.hero-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}
.btn {
  padding: 0.7rem 2rem;
  border-radius: 6px;
  font-weight: bold;
  text-decoration: none;
  transition: background 0.2s;
  border: none;
  display: inline-block;
}
.btn.primary {
  background: #1abc9c;
  color: #fff;
}
.btn.secondary {
  background: #fff;
  color: #0a4d6e;
  border: 2px solid #0a4d6e;
}
.btn:hover {
  opacity: 0.9;
}
.main-content.centered {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 2rem auto;
  max-width: 1200px;
  padding: 0 1rem;
}
.cataract-info {
  margin-top: 2rem;
  max-width: 700px;
  background: #f5faff;
  padding: 1.5rem 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  text-align: left;
}
.cataract-info h2 {
  color: #1976d2;
  margin-bottom: 1rem;
}
.cataract-info a {
  color: #1976d2;
  text-decoration: underline;
}
</style> 