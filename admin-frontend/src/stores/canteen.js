import { defineStore } from 'pinia'
import { ref } from 'vue'
import { submitCanteen, getCanteenRecords, correctCanteenRecord } from '@/api/canteen'

export const useCanteenStore = defineStore('canteen', () => {
  const records = ref([])
  const loading = ref(false)
  const submitting = ref(false)
  const error = ref(null)

  async function load() {
    loading.value = true
    error.value = null
    try {
      records.value = await getCanteenRecords()
    } catch (e) {
      error.value = e.response?.data?.detail || e.message || '加载失败'
    } finally {
      loading.value = false
    }
  }

  async function submit(formData) {
    submitting.value = true
    error.value = null
    try {
      const result = await submitCanteen(formData)
      await load()
      return result
    } catch (e) {
      error.value = e.response?.data?.detail || e.message || '提交失败'
      throw e
    } finally {
      submitting.value = false
    }
  }

  async function correct(id, data) {
    error.value = null
    try {
      await correctCanteenRecord(id, data)
      await load()
    } catch (e) {
      error.value = e.response?.data?.detail || e.message || '更正失败'
      throw e
    }
  }

  return { records, loading, submitting, error, load, submit, correct }
})
