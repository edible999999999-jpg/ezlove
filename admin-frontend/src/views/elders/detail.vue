<template>
  <div>
    <!-- Back link -->
    <div class="mb-6">
      <button class="inline-flex items-center gap-1 text-sm text-on-surface-variant hover:text-primary transition-colors" @click="$router.back()">
        <span class="material-symbols-outlined text-lg">arrow_back</span>
        <span>返回档案列表</span>
      </button>
    </div>

    <template v-if="store.current">
      <!-- Profile Card -->
      <div class="bg-white rounded-3xl shadow-sm border border-outline-variant/20 overflow-hidden mb-6">
        <div class="flex items-center gap-5 p-8 bg-gradient-to-r from-surface-container to-surface border-b border-outline-variant/20">
          <div
            :class="[
              'w-16 h-16 rounded-2xl flex items-center justify-center font-headline text-2xl font-bold text-white shrink-0 shadow-md',
              store.current.care_level === 'A' ? 'bg-primary' : store.current.care_level === 'B' ? 'bg-accent' : 'bg-secondary'
            ]"
          >
            {{ store.current.elder_name?.charAt(0) || '?' }}
          </div>
          <div class="min-w-0">
            <h2 class="font-headline text-2xl font-bold text-on-surface mb-1">{{ store.current.elder_name }}</h2>
            <div class="flex items-center gap-2">
              <span
                :class="[
                  'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold',
                  store.current.care_level === 'A' ? 'bg-primary/10 text-primary' : store.current.care_level === 'B' ? 'bg-accent/10 text-accent' : 'bg-secondary/10 text-secondary'
                ]"
              >
                {{ store.current.care_level }}级
              </span>
              <span class="text-inactive-gray">·</span>
              <span class="text-sm text-on-surface-variant">{{ store.current.address || '未分配地址' }}</span>
            </div>
          </div>
        </div>

        <div class="p-8">
          <dl class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <dt class="text-xs font-bold text-on-surface-variant uppercase tracking-wider mb-1">手机号</dt>
              <dd class="text-sm text-on-surface">{{ store.current.elder_phone || '—' }}</dd>
            </div>
            <div>
              <dt class="text-xs font-bold text-on-surface-variant uppercase tracking-wider mb-1">紧急联系人</dt>
              <dd class="text-sm text-on-surface">{{ store.current.emergency_contact_name || '—' }}</dd>
            </div>
            <div>
              <dt class="text-xs font-bold text-on-surface-variant uppercase tracking-wider mb-1">紧急联系电话</dt>
              <dd class="text-sm text-on-surface">{{ store.current.emergency_contact_phone || '—' }}</dd>
            </div>
            <div>
              <dt class="text-xs font-bold text-on-surface-variant uppercase tracking-wider mb-1">建档时间</dt>
              <dd class="text-sm text-on-surface">{{ formatDate(store.current.created_at) }}</dd>
            </div>
            <div class="md:col-span-2">
              <dt class="text-xs font-bold text-on-surface-variant uppercase tracking-wider mb-1">健康备注</dt>
              <dd class="text-sm text-on-surface">{{ store.current.health_notes || '暂无记录' }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Activity & Events Sections -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white rounded-2xl shadow-sm border border-outline-variant/20 p-6">
          <h3 class="font-headline text-lg font-bold text-on-surface mb-4">近期活动</h3>
          <div class="flex flex-col items-center justify-center py-12 gap-3 text-inactive-gray">
            <span class="material-symbols-outlined text-4xl">calendar_month</span>
            <p class="text-sm">活动日历功能开发中</p>
          </div>
        </div>
        <div class="bg-white rounded-2xl shadow-sm border border-outline-variant/20 p-6">
          <h3 class="font-headline text-lg font-bold text-on-surface mb-4">事件记录</h3>
          <div class="flex flex-col items-center justify-center py-12 gap-3 text-inactive-gray">
            <span class="material-symbols-outlined text-4xl">notifications</span>
            <p class="text-sm">事件时间线功能开发中</p>
          </div>
        </div>
      </div>
    </template>

    <div v-else-if="loading" class="flex items-center justify-center py-20">
      <div class="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin"></div>
    </div>
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

function formatDate(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('zh-CN')
}
</script>
