<template>
    <div class="category__page">
        <div class="main-window">
            <div class="ordering">
                <ProductOrder @select-order="chooseOrder"/>
            </div>

            <div class="content">
                <ProductFilter :data="store.brands" @update-brands="handleBrandsChange"/>
                <CarouselProducts v-if="store.productsForCategoryList.length > 0" 
                :key="currentSlug" 
                :products="store.productsForCategoryList" />
            </div>
            <div class="loading-overlay" v-if="store.loadingCategory">
                <p>Идет загрузка...</p>
            </div>
        </div>
    </div>
    <div ref="LoadingTrigger" v-if="store.nextPageURLCategory" class="loading-trigger">
        <div class="loader" v-if="store.loadingCategory">
            Загрузка...
        </div>
        <div v-else class="trigger-placeholder">
            Загрузить ещё
        </div>
    </div>
</template>

<script setup>
import CarouselProducts from './Child/CarouselProducts.vue';
import ProductFilter from './Child/ProductFilter.vue';
import ProductOrder from './Child/ProductOrder.vue';

import { useProducts } from '@/stores/products';
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router'


const route = useRoute()
const store = useProducts()

const currentSlug = computed(() => {
    return route.params.categorySlug
})

const LoadingTrigger = ref(null)

const selectedBrands = ref([])
const orderFilter = ref(null)

const chooseOrder = async (order) => {orderFilter.value = order}

const handleBrandsChange = async (brandsArray) => {
    selectedBrands.value = brandsArray}

const loadData = async (reset = true) => {
    const slug = currentSlug.value
    if (!slug) return
    
    const brands = selectedBrands.value.join(',')
    await store.getProductCategory(slug, reset, brands)
}

const observer = new IntersectionObserver((entires) => {
  entires.forEach(entry => {
    if (entry.isIntersecting && store.nextPageURLCategory) {
      loadData(false)
    }
  });
}, {threshold: 0.5});


onMounted(() => {
    loadData(true);
    if (LoadingTrigger.value) observer.observe(LoadingTrigger.value)
});

watch(orderFilter, (newOrder) => {
    if (newOrder !== null) {
        store.setOrderCatBy(currentSlug, newOrder)
        loadData(false)
    }
})

watch(selectedBrands, () => {
    loadData(true)
}, { deep: true })

watch(currentSlug, (newSlug, oldSlug) => {
    if (newSlug && newSlug !== oldSlug) {
        loadData(true)
    }
})

onUnmounted(() => {
    if (observer) {
        if (LoadingTrigger.value) {
            observer.unobserve(LoadingTrigger.value)
        }
        observer.disconnect()
    }
    store.resetCategoryProduct()
})
</script>

<style scoped>
.main-window {
    min-height: 800px;
    max-width: 1400px;
    margin: 0 auto;
    padding-left: 300px;

    .content {
        margin-top: 10px;
    }
}
</style>