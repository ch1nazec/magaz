<template>
    <div class="brands__header_main">
        <div class="brand__cart" v-for="value in store.brands.slice(0, 5)">
        <router-link :to="{ name: 'brand', params: { 'searchBrand': value.slug}}">
            <img width="100" height="100" :src="value.logo" alt="">
        </router-link>
        </div>

        <router-link class="a__all__brands" :to="categories">
            <button class="btn__all__brands">Все бренды</button>
        </router-link>
    </div>
</template>

<script setup>
import { useBrandsStore } from '@/stores/brands';
import { onMounted, ref } from 'vue';

const categories = ref([])
const store = useBrandsStore()

onMounted(() => {
    store.getBrands()
})

// export default {
//     setup() {
//         const store = useBrandsStore()
//         onMounted(() => {
//             store.getBrands()
//         })
//         return { store }
//     }
// }
</script>


<style>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.brands__header_main {
    animation: fadeIn 1s forwards;
    display: flex;
    justify-content: space-evenly;
    flex-wrap: wrap;
    align-items: center;
    transition: transform 0.3s ease;
}

.brands__header_main img {
    transition: all 0.3s ease;
}

.brands__header_main img:hover {
    animation: fadeIn 0.3s ease forwards;
}

.btn__all__brands {
    border: none;
    padding: 20px 40px;
    border-radius: 5px;
    background-color: #EBEBEB;
    cursor: pointer;
    transition: background-color 0.4s ease;

    &:hover {
        background-color: #BFBFBF;
    }
}

.a__all__brands {
    margin: 20px 0px;
}
</style>