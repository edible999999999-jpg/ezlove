<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="layout-aside">
      <div class="logo">易挂念 · 社区</div>
      <el-menu :default-active="route.path" router>
        <el-menu-item index="/dashboard">
          <el-icon><DataBoard /></el-icon>
          <span>看板</span>
        </el-menu-item>
        <el-menu-item index="/elders">
          <el-icon><User /></el-icon>
          <span>老人档案</span>
        </el-menu-item>
        <el-menu-item index="/canteen">
          <el-icon><Food /></el-icon>
          <span>食堂管理</span>
        </el-menu-item>
        <el-menu-item index="/events">
          <el-icon><Bell /></el-icon>
          <span>事件中心</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="layout-header">
        <span>{{ userStore.worker?.name }} · {{ userStore.worker?.role_label }}</span>
        <el-button text @click="userStore.logout()">退出</el-button>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { DataBoard, User, Food, Bell } from '@element-plus/icons-vue'

const route = useRoute()
const userStore = useUserStore()
</script>

<style lang="scss" scoped>
.layout-container { min-height: 100vh; }
.layout-aside {
  background: #304156;
  .logo {
    height: 60px;
    line-height: 60px;
    text-align: center;
    color: #fff;
    font-size: 18px;
    font-weight: bold;
  }
  .el-menu { border-right: none; }
}
.layout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
}
</style>
