<script setup>
import { computed } from 'vue';
import { RouterLink, RouterView, useRoute } from 'vue-router'
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';


const route = useRoute()
</script>

<template>
  <div class="wrapper">
    <Header />
      <div class="content">
        <RouterView />
      </div>
    <footer><Footer /></footer>
  </div>
  
</template>

<style>
@import './assets/main.css';

.wrapper {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    margin: 0;
}

.content {
  flex: 1
}
</style>
