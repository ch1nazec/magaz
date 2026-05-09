<template>
    <div class="search__page">
        <div class="main-window">
            <div class="ordering">
                <ProductOrder @select-order="orderParams"/>
            </div>
            
            <CarouselProducts :products="store.products" :totalCount="store.productsCount"  />
        </div>
    </div>

    <div ref="LoadingTrigger" v-if="store.hasMore" class="loading-trigger">
        <div class="loader" v-if="store.loading">
            Загрузка...
        </div>
        <div v-else class="trigger-placeholder">
            Загрузить ещё
        </div>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { nextTick } from 'vue';

import { useProducts } from '@/stores/products';
import CarouselProducts from './Child/CarouselProducts.vue';
import ProductOrder from './Child/ProductOrder.vue';

import { onMounted, onUnmounted, ref, watch } from 'vue';

const store = useProducts()
let observer = null

const route = useRoute()
const LoadingTrigger = ref(null)

const order = ref('')

const createObserver = () => {
    if (observer) {
        observer.disconnect();
    }
    observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting && store.hasMore && !store.loading) {
                    loadProducts(false);
                }
            });
        },
        { threshold: 0.5 }
    );
    
    if (LoadingTrigger.value) {
        observer.observe(LoadingTrigger.value);
    }
}

const orderParams = async (param) => {
    order.value = param
    store.setOrderBy(param)
    
    await nextTick()
    createObserver()
}

const loadProducts = async (reset = false) => {
    if (reset) {
        const searchFromUrl = route.params.searchData || ''
        store.setSearchQuery(searchFromUrl)
        store.setOrderBy(order.value)
        await store.getAllProduct(true)
    }
    else {
        await store.getAllProduct(false)
    }
}

watch(() => route.params.searchData, (newSearch) => {
    const searchValue = newSearch || ''
    
    store.setSearchQuery(searchValue)
    store.getAllProduct(true)

    }, { immediate: true })

onMounted(async () => {
    createObserver()
})

onUnmounted(() => {
    if (LoadingTrigger.value) {
        observer.unobserve(LoadingTrigger.value);
    }
    if (observer) {
        observer.disconnect();
    }

    store.resetProducts()
})
</script>

<style scoped>
.main-window {
    min-height: 800px;
    max-width: 1400px;
    margin: 0 auto;
    padding-left: 250px;

    .content {
        margin-top: 10px;
    }
}
</style>