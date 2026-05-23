import './assets/main.css'
import 'swiper/vue'

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createBootstrap } from 'bootstrap-vue-next'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'

import App from './App.vue'
import router from './router'
import VueLazyload from 'vue-lazyload'


const app = createApp(App)
const pinia = createPinia()

app.use(VueLazyload, {
    preLoad: 1.3,
    error: '@\src\assets\error-icon.svg',
    loading: '@\src\assets\loading.gif',
    attempt: 1})

pinia.use(piniaPluginPersistedstate)
app.use(pinia)

app.use(router)
app.use(createBootstrap)

app.mount('#app')
