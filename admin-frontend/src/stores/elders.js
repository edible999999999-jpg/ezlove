import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getElders, createElder, updateElder, getElder } from '@/api/community'

export const useEldersStore = defineStore('elders', () => {
  const elders = ref([])
  const current = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function load(params) {
    loading.value = true
    error.value = null
    try {
      elders.value = await getElders(params)
    } catch (e) {
      error.value = e.response?.data?.detail || e.message || '加载失败'
    } finally {
      loading.value = false
    }
  }

  async function loadDetail(id) {
    error.value = null
    try {
      current.value = await getElder(id)
    } catch (e) {
      error.value = e.response?.data?.detail || e.message || '加载失败'
    }
  }

  async function create(data) {
    error.value = null
    try {
      await createElder(data)
      await load()
    } catch (e) {
      error.value = e.response?.data?.detail || e.message || '创建失败'
      throw e
    }
  }

  async function update(id, data) {
    error.value = null
    try {
      await updateElder(id, data)
      await load()
    } catch (e) {
      error.value = e.response?.data?.detail || e.message || '更新失败'
      throw e
    }
  }

  return { elders, current, loading, error, load, loadDetail, create, update }
})
