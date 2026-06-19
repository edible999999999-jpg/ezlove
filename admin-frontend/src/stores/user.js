import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi } from '@/api/auth'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  const worker = ref(JSON.parse(localStorage.getItem('community_worker') || 'null'))
  const token = ref(localStorage.getItem('community_access_token') || '')

  const isLoggedIn = computed(() => !!token.value)

  async function login(phone, password) {
    const data = await loginApi(phone, password)
    token.value = data.access_token
    worker.value = data.worker
    localStorage.setItem('community_access_token', data.access_token)
    if (data.refresh_token) {
      localStorage.setItem('community_refresh_token', data.refresh_token)
    }
    localStorage.setItem('community_worker', JSON.stringify(data.worker))
    router.push('/')
  }

  function logout() {
    token.value = ''
    worker.value = null
    localStorage.removeItem('community_access_token')
    localStorage.removeItem('community_refresh_token')
    localStorage.removeItem('community_worker')
    router.push('/login')
  }

  return { worker, token, isLoggedIn, login, logout }
})
