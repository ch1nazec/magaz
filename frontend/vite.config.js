import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vueDevTools from 'vite-plugin-vue-devtools'
import basicSsl from '@vitejs/plugin-basic-ssl'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    // basicSsl(),
  ],
  server: {
    // https: true,
    host: true,
    port: 8080, // Ваш порт для фронтенда,
    allowedHosts: true, 
    proxy: {
      // Все запросы, начинающиеся с /api, Vite перенаправит на Django
      '/api':   { target: 'http://127.0.0.1:8000', changeOrigin: true, secure: false },
      '/media': { target: 'http://127.0.0.1:8000', changeOrigin: true, secure: false },
      '/static':{ target: 'http://127.0.0.1:8000', changeOrigin: true, secure: false },
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
