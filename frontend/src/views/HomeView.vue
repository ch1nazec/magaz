<script setup>
import TheWelcome from '../components/TheWelcome.vue'
import Header from '../components/Header.vue';
import CategoryHeader from '@/components/CategoryHeader.vue';
</script>

<template>
    <Header />
    <div class="main-window">
        <CategoryHeader />
    </div>
</template>

<style>
.main-window {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 100px;
}
</style>