import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/category/:categorySlug',
      name: 'category',
      component: () => import('@/components/Category.vue'),
    },
    {
      path: '/product/search/:searchData',
      name: 'search',
      component: () => import('@/components/SearchProduct.vue')
    },
    {
      path: '/product/brand/:searchBrand',
      name: 'brand',
      component: () => import('@/components/Brands.vue')
    },
    {
      path: '/product/:productSlug',
      name: 'product',
      component: () => import('@/components/Product.vue')
    },
    {
      path: '/login/',
      name: 'login',
      component: () => import('@/components/Login.vue')
    },
  ],
})

export default router
