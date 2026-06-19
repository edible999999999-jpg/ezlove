import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getElders, createElder, updateElder, getElder } from '@/api/community'

export const useEldersStore = defineStore('elders', () => {
  const elders = ref([])
  const current = ref(null)
  const loading = ref(false)

  async function load(params) {
    loading.value = true
    try {
      elders.value = await getElders(params)
    } finally {
      loading.value = false
    }
  }

  async function loadDetail(id) {
    current.value = await getElder(id)
  }

  async function create(data) {
    await createElder(data)
    await load()
  }

  async function update(id, data) {
    await updateElder(id, data)
    await load()
  }

  return { elders, current, loading, load, loadDetail, create, update }
})
