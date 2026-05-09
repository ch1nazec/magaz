<template>
<CarouselProducts :products="storeProducts.products" />

<div ref="LoadingTrigger" v-if="storeProducts.nextPageURL" class="loading-trigger">
  <div class="loader" v-if="storeProducts.loading">
    Загрузка...
  </div>
  <div v-else class="trigger-placeholder">
    Загрузить ещё
  </div>
</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useProducts } from '@/stores/products';
import CarouselProducts from './Child/CarouselProducts.vue';


const storeProducts = useProducts();
const LoadingTrigger = ref(null);

const observer = new IntersectionObserver((entires) => {
  entires.forEach(entry => {
    if (entry.isIntersecting && storeProducts.nextPageURL) {
      storeProducts.getAllProduct();
    }
  });
}, {threshold: 0.5});


onMounted(() => {
  storeProducts.getAllProduct();
  if (LoadingTrigger.value) observer.observe(LoadingTrigger.value)
})

onUnmounted(() => {
  if (LoadingTrigger.value) observer.unobserve(LoadingTrigger.value)
})
</script>
