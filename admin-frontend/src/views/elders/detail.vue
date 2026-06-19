<template>
  <div v-loading="loading">
    <div class="page-header">
      <h2>老人详情</h2>
      <el-button @click="$router.back()">返回</el-button>
    </div>

    <el-card v-if="store.current" class="detail-card">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="姓名">{{ store.current.elder_name }}</el-descriptions-item>
        <el-descriptions-item label="分级">
          <el-tag :type="levelTagType(store.current.care_level)">{{ store.current.care_level }}级</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="手机号">{{ store.current.elder_phone }}</el-descriptions-item>
        <el-descriptions-item label="地址">{{ store.current.address }}</el-descriptions-item>
        <el-descriptions-item label="紧急联系人">{{ store.current.emergency_contact_name }}</el-descriptions-item>
        <el-descriptions-item label="紧急联系电话">{{ store.current.emergency_contact_phone }}</el-descriptions-item>
        <el-descriptions-item label="健康备注" :span="2">{{ store.current.health_notes }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useEldersStore } from '@/stores/elders'

const route = useRoute()
const store = useEldersStore()
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    await store.loadDetail(route.params.id)
  } finally {
    loading.value = false
  }
})

function levelTagType(level) {
  return { A: 'danger', B: 'warning', C: 'success' }[level] || 'info'
}
</script>

<style scoped>
.detail-card { max-width: 800px; }
</style>
