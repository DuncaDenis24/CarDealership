import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  server: {
    proxy: {
      // Route AI chat requests to the AI service
      '/api/chat': {
        target: 'http://localhost:3001',
        changeOrigin: true,
        secure: false
      },
      // Route all other API requests to the main backend
      '^/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
        secure: false
      }
    },
    cors: true
  }
})
