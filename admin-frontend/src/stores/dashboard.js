import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getDashboard } from '@/api/community'

export const useDashboardStore = defineStore('dashboard', () => {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function load() {
    loading.value = true
    error.value = null
    try {
      data.value = await getDashboard()
    } catch (e) {
      error.value = e.response?.data?.detail || e.message || '加载失败'
    } finally {
      loading.value = false
    }
  }

  return { data, loading, error, load }
})
