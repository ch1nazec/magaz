<template>
<div class="brands__page">
        <div class="main-window">
            <div class="ordering">
                <ProductOrder @select-order="orderParams"/>
            </div>
            
            <CarouselProducts :products="store.brandsFilter" :totalCount="store.countTotal"  />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useBrandsStore } from '@/stores/brands';

import CarouselProducts from './Child/CarouselProducts.vue';
import ProductOrder from './Child/ProductOrder.vue';


const route = useRoute()
const store = useBrandsStore();

let observer = null
const LoadingTrigger = ref(null)


const orderParams = async (value) => {
  store.setOrderBy(value)};

const loadProductsBrands = async (flag = false) => {
    const slug = route.params.searchBrand
    if (flag) {
        store.resetProductsBrand()}

    if (slug) {
        await store.getProductsBrand(slug, flag)
    }
}

onMounted(async () => {
    await loadProductsBrands(false)})

watch(() => route.params.searchBrand, () => {
    loadProductsBrands(true)})
</script>

<style>

</style>