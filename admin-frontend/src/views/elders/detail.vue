<template>
  <div v-loading="loading">
    <div class="page-header">
      <div class="back-link" @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        <span>返回档案列表</span>
      </div>
    </div>

    <template v-if="store.current">
      <!-- Profile Card -->
      <div class="profile-card animate-fade-in-up">
        <div class="profile-header">
          <div class="profile-avatar" :class="`avatar--${store.current.care_level?.toLowerCase()}`">
            {{ store.current.elder_name?.charAt(0) || '?' }}
          </div>
          <div class="profile-info">
            <h2 class="profile-name">{{ store.current.elder_name }}</h2>
            <div class="profile-meta">
              <span class="care-badge" :class="`care-badge--${store.current.care_level?.toLowerCase()}`">
                {{ store.current.care_level }}级
              </span>
              <span class="meta-sep">·</span>
              <span class="meta-text">{{ store.current.address || '未分配地址' }}</span>
            </div>
          </div>
        </div>

        <div class="profile-body">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="手机号">{{ store.current.elder_phone || '—' }}</el-descriptions-item>
            <el-descriptions-item label="紧急联系人">{{ store.current.emergency_contact_name || '—' }}</el-descriptions-item>
            <el-descriptions-item label="紧急联系电话">{{ store.current.emergency_contact_phone || '—' }}</el-descriptions-item>
            <el-descriptions-item label="建档时间">{{ formatDate(store.current.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="健康备注" :span="2">
              {{ store.current.health_notes || '暂无记录' }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </div>

      <!-- Activity & Events Sections (placeholder for future API) -->
      <div class="detail-grid animate-fade-in-up" style="animation-delay: 120ms">
        <div class="detail-section">
          <h3 class="section-title">近期活动</h3>
          <div class="empty-state">
            <el-icon :size="32" color="#C4BAB0"><Calendar /></el-icon>
            <p>活动日历功能开发中</p>
          </div>
        </div>
        <div class="detail-section">
          <h3 class="section-title">事件记录</h3>
          <div class="empty-state">
            <el-icon :size="32" color="#C4BAB0"><Bell /></el-icon>
            <p>事件时间线功能开发中</p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useEldersStore } from '@/stores/elders'
import { ArrowLeft, Calendar, Bell } from '@element-plus/icons-vue'

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

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.back-link {
  display: inline-flex;
  align-items: center;
  gap: $sp-1;
  font-size: $fs-sm;
  color: $text-secondary;
  cursor: pointer;
  transition: color $duration-fast $ease-out;

  &:hover {
    color: $brand-terracotta;
  }
}

.profile-card {
  background: $surface-white;
  border: 1px solid $warm-paper;
  border-radius: $radius-lg;
  overflow: hidden;
  margin-bottom: $sp-5;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: $sp-5;
  padding: $sp-6;
  background: linear-gradient(135deg, $warm-paper 0%, $warm-cream 100%);
  border-bottom: 1px solid $warm-paper;
}

.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: $radius-lg;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: $font-display;
  font-size: $fs-2xl;
  font-weight: $fw-bold;
  color: #fff;
  flex-shrink: 0;
  box-shadow: $shadow-md;
}

.avatar--a { background: linear-gradient(135deg, $level-a 0%, #D4736A 100%); }
.avatar--b { background: linear-gradient(135deg, $level-b 0%, #D4B06A 100%); }
.avatar--c { background: linear-gradient(135deg, $level-c 0%, #7AAF76 100%); }

.profile-info {
  min-width: 0;
}

.profile-name {
  font-family: $font-display;
  font-size: $fs-2xl;
  font-weight: $fw-bold;
  color: $text-primary;
  margin-bottom: $sp-1;
}

.profile-meta {
  display: flex;
  align-items: center;
  gap: $sp-2;
}

.meta-sep {
  color: $text-placeholder;
}

.meta-text {
  font-size: $fs-sm;
  color: $text-secondary;
}

.profile-body {
  padding: $sp-5 $sp-6;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $sp-5;
}

.detail-section {
  background: $surface-white;
  border: 1px solid $warm-paper;
  border-radius: $radius-md;
  padding: $sp-5;
}

.section-title {
  font-family: $font-display;
  font-size: $fs-md;
  font-weight: $fw-semibold;
  color: $text-primary;
  margin-bottom: $sp-4;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: $sp-10 $sp-4;
  gap: $sp-3;
  color: $text-placeholder;
  font-size: $fs-sm;
}

@media (max-width: 768px) {
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
