<template>
  <div class="categories">
    <div
      class="category-card"
      v-for="category in store.categoryTree.slice(0, 5)"
      :key="category.id">
      <router-link :to="{ name: 'category', params: { 'categorySlug': category.slug}}">
        <img
        width="170" height="170"
          v-if="category.image"
          :src="category.image"
          :alt="category.name"
          class="category-image"
        />
        
        <div v-else class="no-image">Нет изображения</div>

        <p class="category-card__name">{{ category.name }}</p>
      </router-link>
    </div>
  </div>
</template>

<script>
import { useCategoryStore } from '@/stores/categories';
import { onMounted } from 'vue';

export default {
    setup() {
        const store = useCategoryStore()

        onMounted(() => {
            store.getCategoryTree()
        })
        return { store }
    }
}
</script>

<style scoped>
.categories {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  justify-content: space-between;
}

.category-card {
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.02);
  }
}

.category-card__name {
  font-weight: 600;
}

a {
  color: inherit;
  text-decoration: none;
}


</style>