import { defineStore } from "pinia";
import { ref } from "vue";
import { getMoments, sendMoment, deleteMoment } from "@/api/moment";

export const useMomentStore = defineStore("moment", () => {
  const moments = ref([]);
  const loading = ref(false);

  async function loadMoments(params = {}) {
    loading.value = true;
    try {
      moments.value = await getMoments(params);
    } finally {
      loading.value = false;
    }
  }

  async function send(data) {
    const result = await sendMoment(data);
    moments.value.unshift(result);
    return result;
  }

  async function remove(id) {
    await deleteMoment(id);
    moments.value = moments.value.filter((m) => m.id !== id);
  }

  return { moments, loading, loadMoments, send, remove };
});
