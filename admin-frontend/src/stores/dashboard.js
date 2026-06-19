import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getDashboard } from '@/api/community'

export const useDashboardStore = defineStore('dashboard', () => {
  const data = ref(null)
  const loading = ref(false)

  async function load() {
    loading.value = true
    try {
      data.value = await getDashboard()
    } finally {
      loading.value = false
    }
  }

  return { data, loading, load }
})
