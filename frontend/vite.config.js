import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '127.0.0.1',
    port: 5173,
    strictPort: true,
    proxy: {
      '/books': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/chatbot': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/login': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/admin': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      },
      '/logout': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true
      }
    }
  }
})
