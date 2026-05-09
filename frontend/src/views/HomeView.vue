<script setup>
import Header from '../components/Header.vue';
import CategoryHeader from '@/components/CategoryHeader.vue';
import BrandHeader from '@/components/BrandHeader.vue';
import ProductsHeader from '@/components/ProductsHeader.vue';
import Footer from '@/components/Footer.vue';
</script>

<template>
    <div class="main-window">
        <CategoryHeader />
        <BrandHeader />
        <ProductsHeader />
    </div>
</template>

<style>
.main-window {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 100px;
}
</style>