<template>
  <div v-loading="store.loading">
    <div class="page-header">
      <div>
        <h2>社区看板</h2>
        <p class="page-desc">今日社区老人活动概况</p>
      </div>
      <el-button @click="store.load()" :icon="Refresh">刷新数据</el-button>
    </div>

    <!-- Stats Row -->
    <div class="stats-grid stagger-children">
      <div
        v-for="stat in stats"
        :key="stat.label"
        class="stat-card animate-fade-in-up"
        :style="{ '--accent': stat.color }"
      >
        <div class="stat-icon">
          <el-icon :size="22"><component :is="stat.icon" /></el-icon>
        </div>
        <div class="stat-body">
          <div class="stat-value">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </div>

    <!-- Heatmap -->
    <div class="heatmap-section animate-fade-in-up" style="animation-delay: 360ms">
      <div class="section-header">
        <h3 class="section-title">老人活跃热力图</h3>
        <div class="heatmap-legend">
          <span class="legend-item">
            <span class="legend-dot legend-dot--active"></span>活跃
          </span>
          <span class="legend-item">
            <span class="legend-dot legend-dot--urgent"></span>A级未活跃
          </span>
          <span class="legend-item">
            <span class="legend-dot legend-dot--inactive"></span>未活跃
          </span>
        </div>
      </div>

      <div v-if="heatmapGroups.length" class="heatmap-container">
        <div v-for="group in heatmapGroups" :key="group.address" class="heatmap-group">
          <div class="group-header">
            <span class="group-icon">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 21h18M3 7v1a3 3 0 006 0V7m0 1a3 3 0 006 0V7m0 1a3 3 0 006 0V7H3l2-4h14l2 4M5 21V10.7M19 21V10.7"/>
              </svg>
            </span>
            <span class="group-label">{{ group.address }}</span>
            <span class="group-count">{{ group.elders.length }}人</span>
          </div>
          <div class="heatmap-grid">
            <el-tooltip
              v-for="e in group.elders"
              :key="e.elder_id"
              :content="`${e.name}（${e.care_level}级）— ${e.today_active ? '今日活跃' : '今日未活跃'}`"
              placement="top"
            >
              <div class="heatmap-cell" :class="cellClass(e)">
                <span class="cell-char">{{ e.name?.charAt(0) || '?' }}</span>
              </div>
            </el-tooltip>
          </div>
        </div>
      </div>
      <div v-else class="heatmap-empty">
        <p>暂无老人数据，请先在「老人档案」中添加老人。</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import { Refresh, UserFilled, FirstAidKit, TrendCharts, Sunny } from '@element-plus/icons-vue'

const store = useDashboardStore()
onMounted(() => store.load())

const stats = computed(() => {
  const d = store.data
  if (!d) return []
  return [
    { label: '总人数', value: d.total_elders, color: '#6B8F71', icon: UserFilled },
    { label: 'A级', value: d.level_a, color: '#C44D3E', icon: FirstAidKit },
    { label: 'B级', value: d.level_b, color: '#C4943E', icon: TrendCharts },
    { label: 'C级', value: d.level_c, color: '#5E8F5A', icon: UserFilled },
    { label: '今日活跃', value: d.today_active_count, color: '#6B8F71', icon: Sunny },
    { label: '活跃率', value: `${d.today_active_rate}%`, color: '#5E8F5A', icon: TrendCharts },
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

.page-desc {
  font-size: $fs-sm;
  color: $text-secondary;
  margin-top: $sp-1;
}

// ═══════ Stats Grid ═══════
.stats-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: $sp-4;
  margin-bottom: $sp-6;
}

.stat-card {
  background: $surface-white;
  border: 1px solid $warm-paper;
  border-radius: $radius-md;
  padding: $sp-4 $sp-5;
  display: flex;
  align-items: center;
  gap: $sp-4;
  transition: all $duration-normal $ease-out;

  &:hover {
    box-shadow: $shadow-md;
    border-color: var(--accent, $warm-sand);
    transform: translateY(-2px);
  }
}

.stat-icon {
  width: 44px;
  height: 44px;
  border-radius: $radius-md;
  background: color-mix(in srgb, var(--accent) 10%, transparent);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-body {
  min-width: 0;
}

.stat-value {
  font-family: $font-display;
  font-size: $fs-2xl;
  font-weight: $fw-bold;
  color: $text-primary;
  line-height: $lh-tight;
}

.stat-label {
  font-size: $fs-sm;
  color: $text-secondary;
  margin-top: 2px;
}

// ═══════ Heatmap ═══════
.heatmap-section {
  background: $surface-white;
  border: 1px solid $warm-paper;
  border-radius: $radius-md;
  padding: $sp-5;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $sp-5;
}

.section-title {
  font-family: $font-display;
  font-size: $fs-lg;
  font-weight: $fw-semibold;
  color: $text-primary;
}

.heatmap-legend {
  display: flex;
  gap: $sp-4;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: $sp-1;
  font-size: $fs-sm;
  color: $text-secondary;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: $radius-sm;

  &--active { background: $status-active; }
  &--urgent { background: $level-a; }
  &--inactive { background: $status-inactive; }
}

.heatmap-container {
  display: flex;
  flex-direction: column;
  gap: $sp-5;
}

.heatmap-group {
  padding: $sp-4;
  background: $warm-cream;
  border-radius: $radius-sm;
  border: 1px solid $warm-paper;
}

.group-header {
  display: flex;
  align-items: center;
  gap: $sp-2;
  margin-bottom: $sp-3;
  font-size: $fs-sm;
}

.group-icon {
  color: $text-placeholder;
  display: flex;
}

.group-label {
  font-weight: $fw-semibold;
  color: $text-regular;
}

.group-count {
  color: $text-placeholder;
  font-size: $fs-xs;
  margin-left: $sp-1;
}

.heatmap-grid {
  display: flex;
  flex-wrap: wrap;
  gap: $sp-2;
}

.heatmap-cell {
  width: 52px;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: $radius-sm;
  cursor: pointer;
  transition: all $duration-normal $ease-out;
  position: relative;

  &:hover {
    transform: scale(1.1);
    z-index: 1;
  }

  .cell-char {
    font-size: $fs-lg;
    font-weight: $fw-bold;
    color: #fff;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.15);
  }
}

.cell-active {
  background: linear-gradient(135deg, $status-active 0%, $brand-sage-light 100%);
  box-shadow: 0 2px 8px rgba(94, 143, 90, 0.3);
}

.cell-inactive {
  background: linear-gradient(135deg, $warm-stone 0%, #C4BAB0 100%);
  box-shadow: 0 2px 8px rgba(196, 186, 176, 0.3);
}

.cell-urgent {
  background: linear-gradient(135deg, $level-a 0%, #D4736A 100%);
  box-shadow: 0 2px 8px rgba(196, 77, 62, 0.3);
  animation: pulse-urgent 2s ease-in-out infinite;
}

@keyframes pulse-urgent {
  0%, 100% { box-shadow: 0 2px 8px rgba(196, 77, 62, 0.3); }
  50% { box-shadow: 0 2px 16px rgba(196, 77, 62, 0.5); }
}

.heatmap-empty {
  text-align: center;
  padding: $sp-12 $sp-6;
  color: $text-placeholder;
  font-size: $fs-md;
}

// ═══════ Responsive ═══════
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
