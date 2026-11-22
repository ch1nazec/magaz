<template>
    <div class="window">
        <div class="products">
            <div class="product-detail" v-for="(item, index) in dataProducts.items" :key="item.variant">
                <router-link class="cart-item" :to="{ name: 'product', params: { 'productSlug': item.variant_data.product.slug} }">
                    <img :src="item.variant_data.image" width="200" height="200" alt="..." v-if="item.variant_data.image">
                    <img :src="photoNothing" alt="..." v-else>

                    <p>{{ item.variant_data.product.name }} - {{ item.variant_data.size.name }}</p>
                    <p>Количество - {{ item.quantity }}</p>
                    <p>Цена: {{ item.quantity * item.price }}</p>
                </router-link>
            </div>
        </div>

        <div class="price-detail">
            <div class="totalPrice">Всего: {{ dataProducts.total_price }}</div>
            <div class="totalScore">Количество: {{ dataProducts.total_items }}</div>

            <button class="take__order" @click="takeOrder">Заказать</button>
        </div>
    </div>
</template>

<script setup>
import { useProducts } from '@/stores/products';
import { onMounted, ref } from 'vue';

import photoNothing from '@/assets/photoNothing.png'


const productsStore = useProducts()
const dataProducts = ref([])

const takeOrder = async () => {
    await productsStore.postOrder()}

onMounted(async () => {
    const cart = await productsStore.getCart()
    dataProducts.value = cart})
</script>

<style>
.window {
    display: flex;
    flex-direction: column;

    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.products {
    display: flex;
    flex-direction: column;
    gap: 20px;
}


.product-detail {
    width: 100%;
    min-height: 200px;
    display: flex;
    flex-direction: row;
    border-bottom: 1px solid #eee;
    padding: 20px 0;
}

.cart-item {
    text-decoration: none;
    color: black;
    display: flex;
    gap: 20px;
    align-items: center;
}

.cart-item:hover {
    opacity: 0.8;
}

.empty-cart {
    text-align: center;
    padding: 50px;
}

.loading {
    text-align: center;
    padding: 50px;
}

.price-detail {
    margin-top: 20px;

    margin-left: auto;

    display: flex;
    flex-direction: column;
    gap: 5px;
}

.take__order {
    background: #f3f3f3;

    border: solid 0px;

    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    white-space: nowrap;
    transition: 0.2s;
}

.take__order:hover {
    background: #000;
    color: #fff;
}
</style>