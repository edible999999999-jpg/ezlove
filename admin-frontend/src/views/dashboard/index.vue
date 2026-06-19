<template>
  <div v-loading="store.loading">
    <div class="page-header">
      <div>
        <h2>社区看板</h2>
        <p class="page-desc">今日社区老人活动概况</p>
      </div>
      <el-button @click="store.load()" :icon="Refresh" round>刷新数据</el-button>
    </div>

    <!-- Stats Row -->
    <div class="stats-grid stagger-children">
      <div
        v-for="(stat, i) in stats"
        :key="stat.label"
        class="stat-card animate-fade-in-up"
        :style="{ '--accent': stat.color, '--accent-bg': stat.bgColor, animationDelay: `${i * 60}ms` }"
      >
        <div class="stat-icon">
          <el-icon :size="20"><component :is="stat.icon" /></el-icon>
        </div>
        <div class="stat-body">
          <div class="stat-value">
            <span class="stat-number" :class="{ 'is-percent': stat.isPercent }">{{ animatedValues[stat.key] ?? 0 }}</span>
            <span v-if="stat.isPercent" class="stat-percent">%</span>
          </div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
        <div v-if="stat.ring !== undefined" class="stat-ring">
          <svg width="36" height="36" viewBox="0 0 36 36">
            <circle cx="18" cy="18" r="14" fill="none" :stroke="stat.bgColor" stroke-width="3" />
            <circle
              cx="18" cy="18" r="14"
              fill="none"
              :stroke="stat.color"
              stroke-width="3"
              stroke-linecap="round"
              :stroke-dasharray="`${(stat.ring / 100) * 88} 88`"
              transform="rotate(-90 18 18)"
              class="ring-progress"
            />
          </svg>
        </div>
      </div>
    </div>

    <!-- Two Column: Heatmap + Side Panel -->
    <div class="dashboard-grid">
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
              <div class="group-building">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M3 21h18M5 21V7l8-4v18M19 21V11l-6-4"/>
                  <path d="M9 9h.01M9 12h.01M9 15h.01M9 18h.01"/>
                </svg>
              </div>
              <span class="group-label">{{ group.address }}</span>
              <div class="group-stats">
                <span class="group-count">{{ group.elders.length }}人</span>
                <span class="group-active-rate" :class="group.activeRate > 0 ? 'has-active' : ''">
                  {{ group.activeRate }}% 活跃
                </span>
              </div>
            </div>
            <div class="group-bar">
              <div class="group-bar-fill" :style="{ width: `${group.activeRate}%` }"></div>
            </div>
            <div class="heatmap-grid">
              <div
                v-for="e in group.elders"
                :key="e.elder_id"
                class="heatmap-cell"
                :class="cellClass(e)"
                @click="$router.push(`/elders/${findElderRecordId(e.elder_id)}`)"
              >
                <span class="cell-char">{{ e.name?.charAt(0) || '?' }}</span>
                <span class="cell-level">{{ e.care_level }}</span>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="heatmap-empty">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#C4BAB0" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <path d="M8 15h8M9 9h.01M15 9h.01"/>
          </svg>
          <p>还没有老人数据</p>
          <el-button type="primary" text @click="$router.push('/elders')">去添加第一位老人</el-button>
        </div>
      </div>

      <!-- Side Panel -->
      <div class="side-panel animate-fade-in-up" style="animation-delay: 420ms">
        <!-- Distribution Card -->
        <div class="panel-card">
          <h4 class="panel-title">分级分布</h4>
          <div class="distribution-chart">
            <svg width="120" height="120" viewBox="0 0 120 120" class="donut-chart">
              <circle cx="60" cy="60" r="48" fill="none" stroke="#F5EDE4" stroke-width="12" />
              <circle
                v-for="(seg, i) in donutSegments"
                :key="i"
                cx="60" cy="60" r="48"
                fill="none"
                :stroke="seg.color"
                stroke-width="12"
                stroke-linecap="round"
                :stroke-dasharray="`${seg.length} ${301.6 - seg.length}`"
                :stroke-dashoffset="seg.offset"
                class="donut-segment"
                :style="{ animationDelay: `${i * 200 + 400}ms` }"
              />
              <text x="60" y="56" text-anchor="middle" class="donut-center-value">{{ store.data?.total_elders || 0 }}</text>
              <text x="60" y="72" text-anchor="middle" class="donut-center-label">总计</text>
            </svg>
            <div class="distribution-legend">
              <div v-for="item in distributionData" :key="item.label" class="dist-item">
                <span class="dist-dot" :style="{ background: item.color }"></span>
                <span class="dist-label">{{ item.label }}</span>
                <span class="dist-value">{{ item.value }}人</span>
                <span class="dist-pct">{{ item.pct }}%</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Quick Summary -->
        <div class="panel-card">
          <h4 class="panel-title">今日速览</h4>
          <div class="quick-items">
            <div class="quick-item">
              <div class="quick-icon" style="--qc: #6B8F71">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
              </div>
              <div class="quick-text">
                <span class="quick-label">今日活跃</span>
                <span class="quick-value">{{ store.data?.today_active_count || 0 }} 人查看了消息</span>
              </div>
            </div>
            <div class="quick-item">
              <div class="quick-icon" style="--qc: #C44D3E">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              </div>
              <div class="quick-text">
                <span class="quick-label">需关注</span>
                <span class="quick-value">{{ aLevelInactive }} 位A级老人今日未活跃</span>
              </div>
            </div>
            <div class="quick-item">
              <div class="quick-icon" style="--qc: #D4A24E">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8h1a4 4 0 010 8h-1M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>
              </div>
              <div class="quick-text">
                <span class="quick-label">食堂</span>
                <span class="quick-value">今日暂无就餐记录</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import { useEldersStore } from '@/stores/elders'
import { Refresh, UserFilled, FirstAidKit, TrendCharts, Sunny, CircleCheck } from '@element-plus/icons-vue'

const store = useDashboardStore()
const eldersStore = useEldersStore()
onMounted(() => {
  store.load()
  eldersStore.load()
})

// Animated counters
const animatedValues = ref({})
watch(() => store.data, (newData) => {
  if (!newData) return
  const targets = {
    total: newData.total_elders,
    a: newData.level_a,
    b: newData.level_b,
    c: newData.level_c,
    active: newData.today_active_count,
    rate: newData.today_active_rate,
  }
  Object.entries(targets).forEach(([key, target]) => {
    animateValue(key, target)
  })
}, { immediate: true })

function animateValue(key, target) {
  const duration = 800
  const steps = 30
  const increment = target / steps
  let current = 0
  const interval = setInterval(() => {
    current += increment
    if (current >= target) {
      current = target
      clearInterval(interval)
    }
    animatedValues.value = { ...animatedValues.value, [key]: Number.isInteger(target) ? Math.round(current) : current.toFixed(1) }
  }, duration / steps)
}

const stats = computed(() => {
  const d = store.data
  if (!d) return []
  return [
    { key: 'total', label: '总人数', value: d.total_elders, color: '#2C2825', bgColor: '#F5EDE4', icon: UserFilled },
    { key: 'a', label: 'A级', value: d.level_a, color: '#C44D3E', bgColor: '#FBEAE8', icon: FirstAidKit },
    { key: 'b', label: 'B级', value: d.level_b, color: '#C4943E', bgColor: '#FBF3E8', icon: TrendCharts },
    { key: 'c', label: 'C级', value: d.level_c, color: '#5E8F5A', bgColor: '#E8F3E7', icon: UserFilled },
    { key: 'active', label: '今日活跃', value: d.today_active_count, color: '#6B8F71', bgColor: '#E8F3E7', icon: Sunny, ring: d.today_active_rate },
    { key: 'rate', label: '活跃率', value: d.today_active_rate, color: '#5E8F5A', bgColor: '#E8F3E7', icon: CircleCheck, isPercent: true },
  ]
})

// Heatmap
const heatmapGroups = computed(() => {
  if (!store.data?.heatmap) return []
  const map = {}
  store.data.heatmap.forEach(e => {
    if (!map[e.address]) map[e.address] = []
    map[e.address].push(e)
  })
  return Object.entries(map).map(([address, elders]) => {
    const activeCount = elders.filter(e => e.today_active).length
    return {
      address,
      elders,
      activeRate: elders.length > 0 ? Math.round((activeCount / elders.length) * 100) : 0,
    }
  })
})

const aLevelInactive = computed(() => {
  if (!store.data?.heatmap) return 0
  return store.data.heatmap.filter(e => e.care_level === 'A' && !e.today_active).length
})

// Donut chart
const distributionData = computed(() => {
  const d = store.data
  if (!d || d.total_elders === 0) return []
  return [
    { label: 'A级', value: d.level_a, color: '#C44D3E', pct: Math.round((d.level_a / d.total_elders) * 100) },
    { label: 'B级', value: d.level_b, color: '#C4943E', pct: Math.round((d.level_b / d.total_elders) * 100) },
    { label: 'C级', value: d.level_c, color: '#5E8F5A', pct: Math.round((d.level_c / d.total_elders) * 100) },
  ]
})

const donutSegments = computed(() => {
  const total = store.data?.total_elders || 0
  if (total === 0) return []
  const circumference = 2 * Math.PI * 48  // ~301.6
  let offset = 0
  return distributionData.value.map(item => {
    const length = (item.value / total) * circumference
    const seg = { color: item.color, length, offset: -offset }
    offset += length
    return seg
  })
})

function cellClass(e) {
  if (e.today_active) return 'cell-active'
  if (e.care_level === 'A') return 'cell-urgent'
  return 'cell-inactive'
}

function findElderRecordId(elderUserId) {
  const elder = eldersStore.elders.find(e => e.elder_id === elderUserId)
  return elder?.id || ''
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
  gap: $sp-3;
  transition: all $duration-normal $ease-out;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--accent);
    opacity: 0;
    transition: opacity $duration-normal $ease-out;
  }

  &:hover {
    box-shadow: $shadow-md;
    border-color: var(--accent);
    transform: translateY(-2px);

    &::before {
      opacity: 1;
    }
  }
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: $radius-sm;
  background: var(--accent-bg);
  color: var(--accent);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-body {
  min-width: 0;
  flex: 1;
}

.stat-value {
  display: flex;
  align-items: baseline;
  gap: 1px;
}

.stat-number {
  font-family: $font-display;
  font-size: $fs-2xl;
  font-weight: $fw-bold;
  color: $text-primary;
  line-height: $lh-tight;

  &.is-percent {
    font-size: $fs-xl;
  }
}

.stat-percent {
  font-size: $fs-sm;
  color: $text-secondary;
  font-weight: $fw-medium;
}

.stat-label {
  font-size: $fs-xs;
  color: $text-secondary;
  margin-top: 2px;
  letter-spacing: 0.02em;
}

.stat-ring {
  flex-shrink: 0;

  .ring-progress {
    transition: stroke-dasharray 1s $ease-out;
  }
}

// ═══════ Dashboard Grid ═══════
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: $sp-5;
  align-items: start;
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
  font-size: $fs-xs;
  color: $text-secondary;
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 2px;

  &--active { background: $status-active; }
  &--urgent { background: $level-a; }
  &--inactive { background: $status-inactive; }
}

.heatmap-container {
  display: flex;
  flex-direction: column;
  gap: $sp-4;
}

.heatmap-group {
  padding: $sp-4;
  background: $warm-cream;
  border-radius: $radius-sm;
  border: 1px solid $warm-paper;
  transition: border-color $duration-normal $ease-out;

  &:hover {
    border-color: $warm-sand;
  }
}

.group-header {
  display: flex;
  align-items: center;
  gap: $sp-2;
  margin-bottom: $sp-2;
}

.group-building {
  color: $text-placeholder;
  display: flex;
  flex-shrink: 0;
}

.group-label {
  font-size: $fs-sm;
  font-weight: $fw-semibold;
  color: $text-primary;
}

.group-stats {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: $sp-3;
}

.group-count {
  font-size: $fs-xs;
  color: $text-placeholder;
}

.group-active-rate {
  font-size: $fs-xs;
  color: $text-placeholder;
  font-weight: $fw-medium;

  &.has-active {
    color: $status-active;
  }
}

.group-bar {
  height: 3px;
  background: $warm-paper;
  border-radius: $radius-full;
  margin-bottom: $sp-3;
  overflow: hidden;
}

.group-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, $status-active, $brand-sage-light);
  border-radius: $radius-full;
  transition: width 1s $ease-out;
  min-width: 0;
}

.heatmap-grid {
  display: flex;
  flex-wrap: wrap;
  gap: $sp-2;
}

.heatmap-cell {
  width: 48px;
  height: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: $radius-sm;
  cursor: pointer;
  transition: all $duration-normal $ease-out;
  position: relative;

  &:hover {
    transform: scale(1.12);
    z-index: 1;
    box-shadow: $shadow-md;
  }

  .cell-char {
    font-size: $fs-md;
    font-weight: $fw-bold;
    color: #fff;
    line-height: 1;
  }

  .cell-level {
    font-size: 9px;
    color: rgba(255, 255, 255, 0.7);
    font-weight: $fw-medium;
    margin-top: 1px;
    line-height: 1;
  }
}

.cell-active {
  background: linear-gradient(135deg, $status-active 0%, $brand-sage-light 100%);
  box-shadow: 0 2px 6px rgba(94, 143, 90, 0.25);
}

.cell-inactive {
  background: linear-gradient(135deg, #BDB5AC 0%, #C4BAB0 100%);
  box-shadow: 0 2px 6px rgba(196, 186, 176, 0.2);
}

.cell-urgent {
  background: linear-gradient(135deg, $level-a 0%, #D4736A 100%);
  box-shadow: 0 2px 6px rgba(196, 77, 62, 0.25);
  animation: pulse-urgent 2.5s ease-in-out infinite;
}

@keyframes pulse-urgent {
  0%, 100% { box-shadow: 0 2px 6px rgba(196, 77, 62, 0.25); }
  50% { box-shadow: 0 2px 14px rgba(196, 77, 62, 0.45); }
}

.heatmap-empty {
  text-align: center;
  padding: $sp-16 $sp-6;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $sp-3;

  p {
    color: $text-placeholder;
    font-size: $fs-sm;
  }
}

// ═══════ Side Panel ═══════
.side-panel {
  display: flex;
  flex-direction: column;
  gap: $sp-5;
}

.panel-card {
  background: $surface-white;
  border: 1px solid $warm-paper;
  border-radius: $radius-md;
  padding: $sp-5;
}

.panel-title {
  font-family: $font-display;
  font-size: $fs-md;
  font-weight: $fw-semibold;
  color: $text-primary;
  margin-bottom: $sp-4;
}

// — Donut Chart —
.distribution-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $sp-4;
}

.donut-chart {
  .donut-segment {
    stroke-dasharray: 0 301.6;
    animation: donut-fill 1s $ease-out forwards;
  }

  .donut-center-value {
    font-family: $font-display;
    font-size: 24px;
    font-weight: $fw-bold;
    fill: $text-primary;
  }

  .donut-center-label {
    font-size: 11px;
    fill: $text-secondary;
  }
}

@keyframes donut-fill {
  from { stroke-dasharray: 0 301.6; }
}

.distribution-legend {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: $sp-2;
}

.dist-item {
  display: flex;
  align-items: center;
  gap: $sp-2;
  font-size: $fs-sm;
}

.dist-dot {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  flex-shrink: 0;
}

.dist-label {
  color: $text-regular;
  flex: 1;
}

.dist-value {
  color: $text-primary;
  font-weight: $fw-semibold;
  min-width: 32px;
  text-align: right;
}

.dist-pct {
  color: $text-placeholder;
  font-size: $fs-xs;
  min-width: 32px;
  text-align: right;
}

// — Quick Summary —
.quick-items {
  display: flex;
  flex-direction: column;
  gap: $sp-3;
}

.quick-item {
  display: flex;
  align-items: center;
  gap: $sp-3;
  padding: $sp-3;
  border-radius: $radius-sm;
  background: $warm-cream;
  transition: background $duration-fast $ease-out;

  &:hover {
    background: $warm-paper;
  }
}

.quick-icon {
  width: 32px;
  height: 32px;
  border-radius: $radius-sm;
  background: color-mix(in srgb, var(--qc) 10%, transparent);
  color: var(--qc);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.quick-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.quick-label {
  font-size: $fs-xs;
  color: $text-placeholder;
  font-weight: $fw-medium;
}

.quick-value {
  font-size: $fs-sm;
  color: $text-primary;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

// ═══════ Responsive ═══════
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
