import { defineStore } from 'pinia'
import { ref } from 'vue'
import { submitCanteen, getCanteenRecords, correctCanteenRecord } from '@/api/canteen'

export const useCanteenStore = defineStore('canteen', () => {
  const records = ref([])
  const loading = ref(false)
  const submitting = ref(false)

  async function load() {
    loading.value = true
    try {
      records.value = await getCanteenRecords()
    } finally {
      loading.value = false
    }
  }

  async function submit(formData) {
    submitting.value = true
    try {
      const result = await submitCanteen(formData)
      await load()
      return result
    } finally {
      submitting.value = false
    }
  }

  async function correct(id, data) {
    await correctCanteenRecord(id, data)
    await load()
  }

  return { records, loading, submitting, load, submit, correct }
})
