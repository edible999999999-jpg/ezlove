<template>
  <div v-loading="store.loading">
    <div class="page-header">
      <h2>社区看板</h2>
      <el-button @click="store.load()">刷新</el-button>
    </div>

    <el-row :gutter="16" class="stat-row">
      <el-col :span="4" v-for="stat in stats" :key="stat.label">
        <el-card shadow="hover" class="stat-card" :style="{ borderTop: `3px solid ${stat.color}` }">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="section-card">
      <template #header><span>老人活跃热力图</span></template>
      <div class="heatmap">
        <div v-for="group in heatmapGroups" :key="group.address" class="heatmap-group">
          <div class="group-label">{{ group.address }}</div>
          <div class="heatmap-grid">
            <el-tooltip v-for="e in group.elders" :key="e.elder_id"
              :content="`${e.name} (${e.care_level}级) - ${e.today_active ? '今日活跃' : '今日未活跃'}`">
              <div class="heatmap-cell" :class="cellClass(e)">{{ e.name?.charAt(0) || '?' }}</div>
            </el-tooltip>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()
onMounted(() => store.load())

const stats = computed(() => {
  const d = store.data
  if (!d) return []
  return [
    { label: '总人数', value: d.total_elders, color: '#409EFF' },
    { label: 'A级', value: d.level_a, color: '#F56C6C' },
    { label: 'B级', value: d.level_b, color: '#E6A23C' },
    { label: 'C级', value: d.level_c, color: '#67C23A' },
    { label: '今日活跃', value: d.today_active_count, color: '#409EFF' },
    { label: '活跃率', value: `${d.today_active_rate}%`, color: '#67C23A' },
  ]
})

const heatmapGroups = computed(() => {
  if (!store.data?.heatmap) return []
  const map = {}
  store.data.heatmap.forEach(e => {
    if (!map[e.address]) map[e.address] = []
    map[e.address].push(e)
  })
  return Object.entries(map).map(([address, elders]) => ({ address, elders }))
})

function cellClass(e) {
  if (e.today_active) return 'cell-active'
  if (e.care_level === 'A') return 'cell-urgent'
  return 'cell-inactive'
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;
.stat-row { margin-bottom: 20px; }
.stat-card {
  text-align: center;
  .stat-value { font-size: 28px; font-weight: bold; color: $text-primary; }
  .stat-label { font-size: 14px; color: $text-regular; margin-top: 4px; }
}
.section-card { margin-bottom: 20px; }
.heatmap-group { margin-bottom: 16px; }
.group-label { font-size: 14px; color: $text-regular; margin-bottom: 8px; }
.heatmap-grid { display: flex; flex-wrap: wrap; gap: 8px; }
.heatmap-cell {
  width: 48px; height: 48px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 8px; font-size: 16px; font-weight: bold; color: #fff;
  cursor: pointer;
}
.cell-active { background: #67C23A; }
.cell-inactive { background: #C0C4CC; }
.cell-urgent { background: #F56C6C; }
</style>
