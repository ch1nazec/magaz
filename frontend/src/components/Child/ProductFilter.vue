<template>
    <aside class="sidebar">
        <div class="brands">
            <p class="brands__name">Бренды</p>
            <div class="brands__list">
                <div class="brands__list__brand" v-for="brand in data">
                    <div class="brand__elem">
                        <input type="checkbox" :id="'brand-' + brand.brand_slug" :value="brand.brand_slug" v-model="selectedBrands">
                        <label :for="'brand-' + brand.brand_slug" :class="['brand-label', brand.brand_slug]">{{ brand.brand_name }}</label>
                    </div>
                </div>
            </div>
        </div>
    </aside>
</template>

<script setup>
import { ref, watch, defineEmits } from 'vue';
const props = defineProps({
    data: {
        type: Array,
        required: true,
        default: () => []
    },
})
const emit = defineEmits(['update-brands'])

const selectedBrands = ref([])

watch(selectedBrands, (newVal) => {
    emit('update-brands', newVal)
}, { deep: true });
</script>

<style scoped>
.sidebar {
    position: absolute;
    left: 150px; top: 127px;
    height: 100%;
}

.brand__elem {
    display: flex;
    gap: 5px
}
</style>