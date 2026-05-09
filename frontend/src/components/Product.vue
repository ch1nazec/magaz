<template>
  <div class="main-window">
    <div v-if="first_product" class="product-container">
      <!-- Название товара сверху над всем -->
      <h1 class="display-4 product-title">{{ first_product?.product.name }}</h1>

      <!-- Две колонки: левая (карусель) + правая (размеры) -->
      <div class="product-content">
        <!-- Левая колонка: карусель -->
        <div class="product-carousel">
          <div id="carouselExample" class="carousel slide">
            <div class="carousel-inner">
              <div
                v-for="(image, idx) in first_product?.product.images"
                :key="idx"
                class="carousel-item"
                :class="{ active: idx === 0 }"
              >
                <img
                  v-lazy="image.image"
                  width="300"
                  height="300"
                  class="d-block w-100"
                  :alt="'Фото ' + (idx + 1)"
                />
              </div>
            </div>
            <button
              class="carousel-control-prev"
              type="button"
              data-bs-target="#carouselExample"
              data-bs-slide="prev"
            >
              <span class="carousel-control-prev-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Предыдущий</span>
            </button>
            <button
              class="carousel-control-next"
              type="button"
              data-bs-target="#carouselExample"
              data-bs-slide="next"
            >
              <span class="carousel-control-next-icon" aria-hidden="true"></span>
              <span class="visually-hidden">Следующий</span>
            </button>
          </div>
        </div>

        <!-- Правая колонка: размеры + кнопка -->
        <div class="product-sizes">
          <div class="sizes-grid">
            <div
              v-for="product in products"
              :key="product.size.id"
              class="size-card"
              @click="chooseSize(product.price)"
            >
              <div class="size-name">{{ product.size.name }}</div>
              <div class="size-price">{{ product.price }} ₽</div>
            </div>
          </div>

          <div class="button-price">
            <button v-if="price" type="button" class="btn btn-secondary btn-lg">
              Купить за {{ price }} RUB
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { useRoute } from 'vue-router';
import { useProducts } from '@/stores/products';
import { computed, onMounted, nextTick, ref } from 'vue';


const route = useRoute()
const store = useProducts()

const products = computed(() => {return store.product})
const first_product = computed(() => {return products.value[0]})

const productID = first_product.id

const price = ref(first_product.price)

const productSlug = route.params.productSlug
const checkSlug = computed(() => {
    return productSlug})


const chooseSize = (priceChoose) => {price.value = priceChoose}
onMounted(async () => {
    await nextTick()
    await store.getProduct(checkSlug.value)})
</script>


<style scoped>
.main-window {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 800px;
}

/* Заголовок сверху */
.product-title {
  margin-bottom: 40px;
  text-align: left;
}

/* Две колонки: карусель + размеры */
.product-content {
  display: flex;
  flex-wrap: wrap;
  gap: 48px;
  align-items: flex-start;
}

/* Левая колонка - карусель */
.product-carousel {
  flex: 1;
  min-width: 300px;
}

.carousel.slide {
  max-width: 300px;
}

/* Правая колонка - размеры и кнопка */
.product-sizes {
  flex: 1;
  min-width: 240px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

/* Сетка размеров */
.sizes-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.size-card {
  cursor: pointer;
  border: 1px solid #dee2e6;
  border-radius: 12px;
  padding: 12px 20px;
  text-align: center;
  transition: all 0.2s ease;
  background: white;
  min-width: 90px;
}

.size-card:hover {
  background-color: #f8f9fa;
  border-color: #adb5bd;
  transform: translateY(-2px);
}

.size-name {
  font-weight: 600;
  font-size: 1.1rem;
  margin-bottom: 6px;
}

.size-price {
  color: #2c3e50;
  font-weight: 500;
}

.button-price {
  margin-top: 8px;
}

/* Мобильная адаптация */
@media (max-width: 768px) {
  .product-content {
    flex-direction: column;
  }

  .main-window {
    padding: 20px;
  }

  .sizes-grid {
    justify-content: center;
  }

  .product-title {
    text-align: center;
  }
}
</style>