<template>
  <div>
    <!-- 1. Top Stat Row: 6 cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4 mb-8">
      <!-- Total -->
      <div class="bg-white p-5 rounded-2xl shadow-sm border border-outline-variant/20 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-bold text-inactive-gray tracking-wider uppercase">总人数</span>
          <span class="material-symbols-outlined text-inactive-gray">groups</span>
        </div>
        <div class="serif-num text-3xl font-bold text-on-surface">{{ animatedValues.total ?? 0 }}</div>
      </div>
      <!-- A-Level -->
      <div class="bg-white p-5 rounded-2xl shadow-sm border border-outline-variant/20 hover:shadow-md transition-shadow border-l-4 border-l-primary">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-bold text-primary tracking-wider uppercase">A级</span>
          <span class="material-symbols-outlined text-primary">emergency_home</span>
        </div>
        <div class="serif-num text-3xl font-bold text-on-surface">{{ animatedValues.a ?? 0 }}</div>
      </div>
      <!-- B-Level -->
      <div class="bg-white p-5 rounded-2xl shadow-sm border border-outline-variant/20 hover:shadow-md transition-shadow border-l-4 border-l-accent">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-bold text-accent tracking-wider uppercase">B级</span>
          <span class="material-symbols-outlined text-accent">medical_services</span>
        </div>
        <div class="serif-num text-3xl font-bold text-on-surface">{{ animatedValues.b ?? 0 }}</div>
      </div>
      <!-- C-Level -->
      <div class="bg-white p-5 rounded-2xl shadow-sm border border-outline-variant/20 hover:shadow-md transition-shadow border-l-4 border-l-secondary">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-bold text-secondary tracking-wider uppercase">C级</span>
          <span class="material-symbols-outlined text-secondary">health_and_safety</span>
        </div>
        <div class="serif-num text-3xl font-bold text-on-surface">{{ animatedValues.c ?? 0 }}</div>
      </div>
      <!-- Today Active -->
      <div class="bg-white p-5 rounded-2xl shadow-sm border border-outline-variant/20 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-bold text-on-surface-variant tracking-wider uppercase">今日活跃</span>
          <span class="material-symbols-outlined text-on-surface-variant">bolt</span>
        </div>
        <div class="serif-num text-3xl font-bold text-on-surface">{{ animatedValues.active ?? 0 }}</div>
      </div>
      <!-- Active Rate -->
      <div class="bg-white p-5 rounded-2xl shadow-sm border border-outline-variant/20 hover:shadow-md transition-shadow">
        <div class="flex justify-between items-start mb-2">
          <span class="text-xs font-bold text-on-surface-variant tracking-wider uppercase">活跃率</span>
          <span class="material-symbols-outlined text-on-surface-variant">analytics</span>
        </div>
        <div class="serif-num text-3xl font-bold text-on-surface">{{ animatedValues.rate ?? 0 }}%</div>
      </div>
    </div>

    <!-- Main Layout: Heatmap + Sidebar -->
    <div class="flex flex-col lg:flex-row gap-8">
      <!-- 2. Main Heatmap Section -->
      <div class="flex-1 space-y-8">
        <div class="bg-white p-8 rounded-3xl shadow-sm border border-outline-variant/20">
          <div class="flex justify-between items-center mb-8">
            <div>
              <h3 class="font-headline text-2xl font-bold text-on-surface">老人活跃热力图</h3>
              <p class="text-on-surface-variant text-sm mt-1">实时监测各楼栋长者活动状态</p>
            </div>
            <div class="flex items-center gap-4 text-xs font-medium">
              <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-secondary"></span> 活跃</div>
              <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-primary"></span> A级异常</div>
              <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-inactive-gray"></span> 离线</div>
            </div>
          </div>

          <div v-if="heatmapGroups.length">
            <div v-for="(group, gi) in heatmapGroups" :key="group.address" :class="{ 'mb-10': gi < heatmapGroups.length - 1 }">
              <div class="flex items-end justify-between mb-4 px-1">
                <div>
                  <h4 class="font-headline text-lg font-semibold flex items-center gap-2">
                    {{ group.address }}
                    <span class="text-xs font-normal bg-surface-container px-2 py-0.5 rounded text-on-surface-variant">{{ group.elders.length }} 人</span>
                  </h4>
                </div>
                <div class="text-right">
                  <span class="text-xs font-bold text-on-surface-variant uppercase">活跃 {{ group.activeRate }}%</span>
                  <div class="w-32 h-1.5 bg-surface-container rounded-full mt-1 overflow-hidden">
                    <div class="h-full bg-secondary rounded-full transition-all duration-700" :style="{ width: group.activeRate + '%' }"></div>
                  </div>
                </div>
              </div>
              <div class="flex flex-wrap gap-4">
                <div
                  v-for="e in group.elders"
                  :key="e.elder_id"
                  :class="[
                    'w-12 h-12 text-white flex items-center justify-center rounded-xl font-headline text-lg shadow-sm hover:scale-105 transition-transform cursor-pointer',
                    e.today_active ? 'bg-secondary' : (e.care_level === 'A' ? 'bg-primary ring-4 ring-primary/20' : 'bg-inactive-gray opacity-80')
                  ]"
                  @click="$router.push(`/elders/${findElderRecordId(e.elder_id)}`)"
                >
                  {{ e.name?.charAt(0) || '?' }}
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-16 flex flex-col items-center gap-3">
            <span class="material-symbols-outlined text-5xl text-inactive-gray">sentiment_dissatisfied</span>
            <p class="text-inactive-gray text-sm">还没有老人数据</p>
            <button class="text-primary text-sm font-semibold hover:underline" @click="$router.push('/elders')">去添加第一位老人</button>
          </div>
        </div>

        <!-- Decorative/Atmospheric Element -->
        <div class="relative h-48 rounded-3xl overflow-hidden group bg-gradient-to-br from-[#2C2825] to-[#6B8F71]">
          <div class="absolute inset-0 bg-gradient-to-t from-on-surface/60 to-transparent"></div>
          <div class="absolute bottom-6 left-8">
            <h5 class="text-white font-headline text-xl font-bold">社区康养中心</h5>
            <p class="text-white/80 text-sm">静时已开始，夜班值班中</p>
          </div>
        </div>
      </div>

      <!-- 3. Right Sidebar/Panel -->
      <div class="w-full lg:w-80 space-y-6">
        <!-- Care Distribution Donut -->
        <div class="bg-white p-6 rounded-3xl shadow-sm border border-outline-variant/20">
          <h3 class="font-headline text-lg font-bold text-on-surface mb-6">分级分布</h3>
          <div class="relative w-48 h-48 mx-auto mb-6 flex items-center justify-center">
            <svg class="w-full h-full -rotate-90" viewBox="0 0 36 36">
              <circle cx="18" cy="18" fill="transparent" r="15.9" stroke="#E5DED5" stroke-width="3"></circle>
              <circle v-if="totalElders > 0" cx="18" cy="18" fill="transparent" r="15.9" stroke="#C44D3E"
                :stroke-dasharray="`${(levelA / totalElders) * 100} 100`" stroke-width="3"></circle>
              <circle v-if="totalElders > 0" cx="18" cy="18" fill="transparent" r="15.9" stroke="#D4A24E"
                :stroke-dasharray="`${(levelB / totalElders) * 100} 100`"
                :stroke-dashoffset="`-${(levelA / totalElders) * 100}`" stroke-width="3"></circle>
              <circle v-if="totalElders > 0" cx="18" cy="18" fill="transparent" r="15.9" stroke="#6B8F71"
                :stroke-dasharray="`${(levelC / totalElders) * 100} 100`"
                :stroke-dashoffset="`-${((levelA + levelB) / totalElders) * 100}`" stroke-width="3"></circle>
            </svg>
            <div class="absolute text-center">
              <span class="serif-num text-2xl font-bold block">{{ totalElders }}</span>
              <span class="text-[10px] text-on-surface-variant font-bold uppercase tracking-widest">总计</span>
            </div>
          </div>
          <div class="space-y-3">
            <div class="flex justify-between items-center text-sm">
              <div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-primary"></span> A级（紧急关爱）</div>
              <span class="serif-num font-bold">{{ totalElders > 0 ? ((levelA / totalElders) * 100).toFixed(1) : '0.0' }}%</span>
            </div>
            <div class="flex justify-between items-center text-sm">
              <div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-accent"></span> B级（医疗关注）</div>
              <span class="serif-num font-bold">{{ totalElders > 0 ? ((levelB / totalElders) * 100).toFixed(1) : '0.0' }}%</span>
            </div>
            <div class="flex justify-between items-center text-sm">
              <div class="flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-secondary"></span> C级（日常关爱）</div>
              <span class="serif-num font-bold">{{ totalElders > 0 ? ((levelC / totalElders) * 100).toFixed(1) : '0.0' }}%</span>
            </div>
          </div>
        </div>

        <!-- Today Quick View -->
        <div class="bg-white p-6 rounded-3xl shadow-sm border border-outline-variant/20">
          <h3 class="font-headline text-lg font-bold text-on-surface mb-6">今日速览</h3>
          <div class="space-y-4">
            <!-- Emergency Call -->
            <div class="flex gap-4 p-4 rounded-2xl bg-primary/5 border border-primary/10 hover:bg-primary/10 transition-colors">
              <div class="w-10 h-10 rounded-xl bg-primary flex items-center justify-center shrink-0">
                <span class="material-symbols-outlined text-white">ring_volume</span>
              </div>
              <div>
                <p class="text-sm font-bold text-on-surface">{{ aLevelInactive }} 位A级未活跃</p>
                <p class="text-xs text-on-surface-variant mt-1">需重点关注老人今日状态</p>
              </div>
            </div>
            <!-- Medication Reminders -->
            <div class="flex gap-4 p-4 rounded-2xl bg-accent/5 border border-accent/10 hover:bg-accent/10 transition-colors">
              <div class="w-10 h-10 rounded-xl bg-accent flex items-center justify-center shrink-0">
                <span class="material-symbols-outlined text-white">medication</span>
              </div>
              <div>
                <p class="text-sm font-bold text-on-surface">今日活跃 {{ todayActiveCount }} 人</p>
                <p class="text-xs text-on-surface-variant mt-1">社区老人活动参与情况</p>
              </div>
            </div>
            <!-- Meal Requests -->
            <div class="flex gap-4 p-4 rounded-2xl bg-secondary/5 border border-secondary/10 hover:bg-secondary/10 transition-colors">
              <div class="w-10 h-10 rounded-xl bg-secondary flex items-center justify-center shrink-0">
                <span class="material-symbols-outlined text-white">lunch_dining</span>
              </div>
              <div>
                <p class="text-sm font-bold text-on-surface">食堂就餐</p>
                <p class="text-xs text-on-surface-variant mt-1">今日暂无就餐记录</p>
              </div>
            </div>
          </div>
        </div>

        <!-- System Status -->
        <div class="p-6 bg-surface-container rounded-3xl border border-outline-variant/30 text-center">
          <span class="inline-block w-2 h-2 rounded-full bg-secondary mb-2 animate-pulse"></span>
          <p class="text-xs font-bold text-on-surface tracking-wider uppercase">系统正常</p>
          <p class="text-[10px] text-on-surface-variant mt-1">上次同步: {{ currentTime }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'
import { useEldersStore } from '@/stores/elders'

const store = useDashboardStore()
const eldersStore = useEldersStore()
onMounted(() => {
  store.load()
  eldersStore.load()
})

// Time display
const currentTime = ref(new Date().toLocaleTimeString('zh-CN', { hour12: true }))
let timeInterval
onMounted(() => {
  timeInterval = setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString('zh-CN', { hour12: true })
  }, 1000)
})
onUnmounted(() => clearInterval(timeInterval))

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
    animatedValues.value = {
      ...animatedValues.value,
      [key]: Number.isInteger(target) ? Math.round(current) : Number(current.toFixed(1))
    }
  }, duration / steps)
}

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

const todayActiveCount = computed(() => store.data?.today_active_count || 0)

// Donut chart data
const totalElders = computed(() => store.data?.total_elders || 0)
const levelA = computed(() => store.data?.level_a || 0)
const levelB = computed(() => store.data?.level_b || 0)
const levelC = computed(() => store.data?.level_c || 0)

function findElderRecordId(elderUserId) {
  const elder = eldersStore.elders.find(e => e.elder_id === elderUserId)
  return elder?.id || ''
}
</script>
