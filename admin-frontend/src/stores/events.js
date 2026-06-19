import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getEvents, createEvent, resolveEvent } from '@/api/events'

export const useEventsStore = defineStore('events', () => {
  const events = ref([])
  const loading = ref(false)

  async function load(params) {
    loading.value = true
    try {
      events.value = await getEvents(params)
    } finally {
      loading.value = false
    }
  }

  async function create(data) {
    await createEvent(data)
    await load()
  }

  async function resolve(id) {
    await resolveEvent(id)
    await load()
  }

  return { events, loading, load, create, resolve }
})
