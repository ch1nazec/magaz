<template>
    
    <div class="total__count" v-if="props.totalCount">
        <p class="total__string">Всего: {{ props.totalCount }}</p>
    </div>
    <div class="card-list">
        <div class="card-item" v-for="product in products" :key="product.id">
            <router-link :key="$route.fullPath" :to="{ name: 'product', params: { 'productSlug': product.slug}}" class="a-card">
                <div class="product-card" v-if="!!product.image_main">
                    <img :src="product.image_main" height="200" width="200" :alt="product.name">
                        <div class="name-item">
                            {{ nameProduct(product.name) }}
                        </div>
                        <div class="price">
                            {{ product.price_s }} RUB
                        </div>
                </div>
            </router-link>
        </div>
    </div>
</template>

<script setup>

const props = defineProps({
    products: {
        type: Array,
        required: true,
        default: () => []
    },
    totalCount: {
        type: Number,
        required: false
    }
})

const nameProduct = (name) => {
    const limit = 40
    if (name && name.length > limit) {
        return name.slice(0, limit) + '...'
    }
    return name || ''
}

</script>

<style scoped>
.total__count {
    padding: 20px;

    .total__string {
        font-size: 20px;
    }
}
.a-card {
    text-decoration: none;
    color: inherit;

    border: none !important;
    background: transparent !important;
}

.card-item {
    border: none;
    transition: transform 0.3s ease;
    justify-content: flex-end;

    &:hover {
        transform: scale(1.03);
    }

    width: 200px;
    height: 282px;

    .name-item {
        font-size: 14px;
    }
    .price {
        float: right;
        margin-right: 36px;
    }
}

.card-list {
    display: flex;
    flex-wrap: wrap;
}
</style>