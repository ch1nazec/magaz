<template>
<div class="header">

    <!-- ===== TOP ===== -->
    <div class="header__main">
        
        <div class="header__logo">
            <a href="/">
                <img src="../assets/icon1.png" alt="ABCE">
            </a>
        </div>

        <div class="header__search">
            <input type="text" placeholder="Поиск товаров..." v-model="ssearchData">
            <div class="logo__loop" v-if="ssearchData">
                <router-link class="loop__a" :to="{ name: 'search', params: {'searchData': ssearchData} }">
                    <img src="../assets/loop.png" width="20" height="20" alt="Поиск">
                </router-link>
            </div>
        </div>

        <div class="header__right">
            <a href="/about" class="header__about">О нас</a>

            <div class="other__logo">
                <router-link class="account-page" :to="{ name: 'login' }">
                    <img src="../assets/userheader.svg" alt="Аккаунт">
                </router-link>
                
                <router-link class="cart-page" :to="{ name: 'cart' }">
                    <img src="../assets/favourite.svg" alt="Корзина">
                </router-link>
            </div>
        </div>

    </div>

    <!-- ===== CATEGORY BAR ===== -->
    <div class="header__category"
         @mouseenter="show = true"
         @mouseleave="show = false">

        <div class="category__box">Категории</div>

        <div class="category" ref="scrollContainer">
            <router-link
                v-for="cat in categories"
                :key="cat.id"
                :to="`/category/${cat.slug}/`"
                class="category__a">
                {{ cat.name }}
            </router-link>
        </div>

        <div class="buttons">
            <button @click="scroll('left')" class="carousel-btn">‹</button>
            <button @click="scroll('right')" class="carousel-btn">›</button>
        </div>

        <!-- ===== DROPDOWN ===== -->
        <div class="category-list" v-show="show">
            <div class="category-list__cart"
                 v-for="cat in categoriesTree"
                 :key="cat.id">

                <router-link
                    :to="`/category/${cat.slug}`"
                    class="category-list__main-name">
                    {{ cat.name }}
                </router-link>

                <div class="category__undercategory">
                    <router-link
                        v-for="child in cat.children"
                        :key="child.id"
                        :to="`/category/${child.slug}`"
                        class="category__undercategory_a">
                        {{ child.name }}
                    </router-link>
                </div>

            </div>
        </div>

    </div>

</div>
<div class="empty-place">
</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'
import { useAuthStore } from '@/stores/auth'


const storeAuth = useAuthStore()

const show = ref(false)

const categories = ref([])
const categoriesTree = ref([])

const ssearchData = ref('')
const scrollContainer = ref(null)

const checkSearch = computed(() => {
    console.log(searchData.value)
    ssearchData.value})

const scroll = (dir) => {
    const el = scrollContainer.value
    const amount = 300

    el.scrollBy({
        left: dir === 'left' ? -amount : amount,
        behavior: 'smooth'
    })
}

const getCategories = async () => {
    const { data } = await api.get('categories/')
    categories.value = data
}

const getTreeCategories = async () => {
    const { data } = await api.get('categories/tree/')
    categoriesTree.value = data
}

onMounted(() => {
    getCategories()
    getTreeCategories()
})
</script>

<style scoped>

/* ===== BASE ===== */

* {
    box-sizing: border-box;
}

a {
    text-decoration: none;
    color: inherit;
}
.empty-place {
    margin-top: 127px;
}
.header {
    position: fixed;
    top: 0;
    width: 100%;
    z-index: 100000;
    font-family: 'Inter', sans-serif;
    background: #fff;
    border-bottom: 1px solid #eee;
}

/* ===== TOP ===== */

.header__main {
    max-width: 1200px;
    margin: 0 auto;

    display: flex;
    align-items: center;
    justify-content: space-between;

    height: 70px;
    padding: 0 20px;
}

/* LOGO */
.header__logo img {
    width: 42px;
}

/* SEARCH */
.header__search {
    flex: 1;
    flex-direction: row;
    max-width: 500px;
    margin: 0 40px;
    position: relative;
}

.header__search input {
    width: 100%;
    height: 42px;

    border-radius: 12px;
    border: none;
    background: #f5f5f5;

    padding: 0 45px 0 15px;
    transition: 0.2s;
}

.header__search input:focus {
    background: #fff;
    box-shadow: 0 0 0 2px #000;
    outline: none;
}

.logo__loop {
    position: absolute;
    right: 12px;
    top: 10px;
    opacity: 0.6;
}

/* RIGHT */
.header__right {
    display: flex;
    align-items: center;
    gap: 25px;
}

.header__about {
    font-weight: 500;
}

.other__logo {
    display: flex;
    gap: 15px;
}

.other__logo img {
    width: 24px;
    opacity: 0.7;
    transition: 0.2s;
}

.other__logo img:hover {
    opacity: 1;
    transform: scale(1.1);
}

/* ===== CATEGORY ===== */

.header__category {
    max-width: 1200px;
    margin: 0 auto;

    display: flex;
    align-items: center;
    gap: 15px;

    padding: 10px 20px;
    position: relative;
}

.category__box {
    background: #000;
    color: #fff;
    padding: 8px 16px;
    border-radius: 10px;
    cursor: pointer;
}

.category {
    display: flex;
    gap: 10px;
    overflow-x: auto;
    flex: 1;

    scrollbar-width: none;
    -ms-overflow-style: none;
}

.category::-webkit-scrollbar {
    display: none;
}

.category__a {
    background: #f3f3f3;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    white-space: nowrap;
    transition: 0.2s;
}

.category__a:hover {
    background: #000;
    color: #fff;
}

.buttons {
    display: flex;
    gap: 8px;
}

.carousel-btn {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    border: none;
    background: #000;
    color: #fff;
    cursor: pointer;
}

/* ===== DROPDOWN ===== */

/* .category-list {
    position: absolute;
    top: 100%;
    left: 0;

    width: 100%;

    background: #fff;
    border-top: 1px solid #eee;

    padding: 30px 20px;

    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 40px;

    box-shadow: 0 15px 50px rgba(0,0,0,0.08);

    animation: fade 0.2s ease;
    z-index: 100;
} */

.category-list {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;

    background: #fff;
    border-top: 1px solid #eee;

    padding: 30px 20px;

    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 40px;

    box-shadow: 0 15px 50px rgba(0,0,0,0.08);
    z-index: 100;
}

@keyframes fade {
    from {
        opacity: 0;
        transform: translateY(-8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.category-list__main-name {
    font-weight: 600;
    font-size: 14px;
}

.category__undercategory {
    margin-top: 5px;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.category__undercategory_a {
    font-size: 13px;
    color: #777;
}

.category__undercategory_a:hover {
    color: #000;
}


/* @media (max-width: 900px) {
    .header__search {
        display: none;
    }
} */
</style>