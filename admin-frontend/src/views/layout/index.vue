<template>
  <el-container class="layout-container">
    <!-- Sidebar -->
    <el-aside :width="isCollapsed ? '72px' : '240px'" class="layout-aside">
      <!-- Logo -->
      <div class="aside-logo" :class="{ 'is-collapsed': isCollapsed }">
        <div class="logo-icon">
          <svg width="28" height="28" viewBox="0 0 48 48" fill="none">
            <path d="M24 4C14 4 8 12 8 20c0 6 4 10 8 13v7a2 2 0 002 2h12a2 2 0 002-2v-7c4-3 8-7 8-13C40 12 34 4 24 4z" fill="rgba(199,92,58,0.3)" stroke="rgba(199,92,58,0.8)" stroke-width="1.5"/>
            <circle cx="24" cy="18" r="5" fill="rgba(199,92,58,0.2)" stroke="rgba(199,92,58,0.6)" stroke-width="1.5"/>
            <path d="M24 16v4M22 18h4" stroke="rgba(199,92,58,0.9)" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
        </div>
        <transition name="fade">
          <span v-show="!isCollapsed" class="logo-text">易挂念</span>
        </transition>
      </div>

      <!-- Navigation -->
      <nav class="aside-nav">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="nav-item"
          :class="{ 'is-active': route.path === item.path }"
        >
          <el-icon :size="20"><component :is="item.icon" /></el-icon>
          <transition name="fade">
            <span v-show="!isCollapsed" class="nav-label">{{ item.label }}</span>
          </transition>
          <transition name="fade">
            <span v-if="item.badge && !isCollapsed" class="nav-badge">{{ item.badge }}</span>
          </transition>
        </router-link>
      </nav>

      <!-- Collapse Toggle -->
      <div class="aside-footer">
        <button class="collapse-btn" @click="isCollapsed = !isCollapsed">
          <el-icon :size="18">
            <Fold v-if="!isCollapsed" />
            <Expand v-else />
          </el-icon>
        </button>
      </div>
    </el-aside>

    <!-- Main Content -->
    <el-container class="main-container">
      <!-- Header -->
      <el-header class="layout-header">
        <div class="header-left">
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/dashboard' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentPageName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <div class="header-user">
            <div class="user-avatar">{{ userStore.worker?.name?.charAt(0) || '?' }}</div>
            <div class="user-info">
              <span class="user-name">{{ userStore.worker?.name }}</span>
              <span class="user-role">{{ userStore.worker?.role_label }}</span>
            </div>
          </div>
          <el-button text class="logout-btn" @click="userStore.logout()">
            <el-icon><SwitchButton /></el-icon>
          </el-button>
        </div>
      </el-header>

      <!-- Page Content -->
      <el-main class="layout-main">
        <router-view v-slot="{ Component }">
          <transition name="page-fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  DataBoard, UserFilled, Dish, Bell, Fold, Expand, SwitchButton
} from '@element-plus/icons-vue'

const route = useRoute()
const userStore = useUserStore()
const isCollapsed = ref(false)

const navItems = [
  { path: '/dashboard', label: '看板', icon: DataBoard },
  { path: '/elders', label: '老人档案', icon: UserFilled },
  { path: '/canteen', label: '食堂管理', icon: Dish },
  { path: '/events', label: '事件中心', icon: Bell },
]

const pageNameMap = {
  '/dashboard': '社区看板',
  '/elders': '老人档案',
  '/canteen': '食堂管理',
  '/events': '事件中心',
}

const currentPageName = computed(() => {
  return pageNameMap[route.path] || (route.path.startsWith('/elders/') ? '老人详情' : '')
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.layout-container {
  min-height: 100vh;
}

// ═══════ Sidebar ═══════
.layout-aside {
  background: $dark-hearth;
  display: flex;
  flex-direction: column;
  transition: width $duration-slow $ease-out;
  overflow: hidden;
  position: relative;
  z-index: $z-sidebar;

  &::after {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 1px;
    height: 100%;
    background: linear-gradient(180deg, rgba(199,92,58,0.2) 0%, transparent 50%, rgba(199,92,58,0.1) 100%);
  }
}

.aside-logo {
  display: flex;
  align-items: center;
  gap: $sp-3;
  padding: $sp-5 $sp-4;
  height: 64px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  transition: padding $duration-normal $ease-out;

  &.is-collapsed {
    justify-content: center;
    padding: $sp-5 $sp-2;
  }
}

.logo-icon {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(199, 92, 58, 0.12);
  border-radius: $radius-sm;
  border: 1px solid rgba(199, 92, 58, 0.2);
}

.logo-text {
  font-family: $font-display;
  font-size: $fs-xl;
  font-weight: $fw-bold;
  color: #fff;
  white-space: nowrap;
  letter-spacing: 0.05em;
}

// — Navigation —
.aside-nav {
  flex: 1;
  padding: $sp-3 $sp-2;
  display: flex;
  flex-direction: column;
  gap: $sp-1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: $sp-3;
  padding: $sp-3 $sp-4;
  border-radius: $radius-sm;
  color: rgba(255, 255, 255, 0.55);
  text-decoration: none;
  font-size: $fs-md;
  font-weight: $fw-medium;
  transition: all $duration-normal $ease-out;
  position: relative;
  cursor: pointer;

  &:hover {
    color: rgba(255, 255, 255, 0.85);
    background: rgba(255, 255, 255, 0.05);
  }

  &.is-active {
    color: #fff;
    background: rgba(199, 92, 58, 0.2);

    &::before {
      content: '';
      position: absolute;
      left: 0;
      top: 50%;
      transform: translateY(-50%);
      width: 3px;
      height: 20px;
      background: $brand-terracotta;
      border-radius: 0 $radius-full $radius-full 0;
    }

    .el-icon {
      color: $brand-terracotta-light;
    }
  }

  .el-icon {
    flex-shrink: 0;
    transition: color $duration-normal $ease-out;
  }
}

.nav-label {
  white-space: nowrap;
  overflow: hidden;
}

.nav-badge {
  margin-left: auto;
  background: $brand-terracotta;
  color: #fff;
  font-size: $fs-xs;
  font-weight: $fw-bold;
  padding: 1px 6px;
  border-radius: $radius-full;
  min-width: 18px;
  text-align: center;
}

// — Footer —
.aside-footer {
  padding: $sp-3;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.collapse-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 36px;
  border-radius: $radius-sm;
  border: none;
  background: transparent;
  color: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: all $duration-normal $ease-out;

  &:hover {
    color: rgba(255, 255, 255, 0.7);
    background: rgba(255, 255, 255, 0.05);
  }
}

// ═══════ Main Content ═══════
.main-container {
  background: $warm-cream;
}

.layout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  background: $surface-white;
  border-bottom: 1px solid $warm-paper;
  padding: 0 $sp-6;
  position: sticky;
  top: 0;
  z-index: $z-header;
}

.header-left {
  .el-breadcrumb {
    font-size: $fs-sm;
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: $sp-4;
}

.header-user {
  display: flex;
  align-items: center;
  gap: $sp-3;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: $radius-full;
  background: linear-gradient(135deg, $brand-terracotta 0%, $brand-terracotta-light 100%);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: $fs-sm;
  font-weight: $fw-bold;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: $fs-sm;
  font-weight: $fw-semibold;
  color: $text-primary;
  line-height: 1.2;
}

.user-role {
  font-size: $fs-xs;
  color: $text-secondary;
  line-height: 1.2;
}

.logout-btn {
  color: $text-placeholder;
  padding: $sp-2;

  &:hover {
    color: $text-secondary;
  }
}

.layout-main {
  padding: $sp-6;
  overflow-y: auto;
}

// ═══════ Transitions ═══════
.fade-enter-active,
.fade-leave-active {
  transition: opacity $duration-fast $ease-out;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.page-fade-enter-active {
  transition: opacity $duration-normal $ease-out, transform $duration-normal $ease-out;
}
.page-fade-leave-active {
  transition: opacity $duration-fast $ease-out;
}
.page-fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.page-fade-leave-to {
  opacity: 0;
}
</style>
