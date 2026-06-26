<template>
  <view class="role-page">
    <!-- 氛围背景 -->
    <view class="ambient-bg">
      <view class="ambient-circle ambient-1" />
      <view class="ambient-circle ambient-2" />
    </view>

    <!-- 主内容 -->
    <view class="role-content">
      <!-- Hero -->
      <view class="hero-section fade-in">
        <text class="hero-title">你是</text>
      </view>

      <!-- 角色卡片 -->
      <view class="role-cards">
        <view
          class="role-card fade-in stagger-1"
          :class="{ 'role-card-active': selectedRole === 'family' }"
          @tap="selectedRole = 'family'"
        >
          <image class="role-card-icon" src="/static/icons/family.svg" mode="aspectFit" />
          <text class="role-card-title">子女/亲属</text>
          <text class="role-card-desc">每天发送牵挂，让老人知道你惦记Ta</text>
        </view>

        <view
          class="role-card fade-in stagger-2"
          :class="{ 'role-card-active': selectedRole === 'elder' }"
          @tap="selectedRole = 'elder'"
        >
          <image class="role-card-icon" src="/static/icons/elderly.svg" mode="aspectFit" />
          <text class="role-card-title">长辈</text>
          <text class="role-card-desc">查看孩子们的问候，用表情回应关爱</text>
        </view>
      </view>

      <!-- 确认按钮 -->
      <view class="confirm-area" :class="{ visible: selectedRole }">
        <button class="confirm-btn" @tap="confirmRole">
          <text class="confirm-btn-text">开启挂念之旅</text>
        </button>
      </view>
    </view>

    <!-- Footer -->
    <view class="role-footer fade-in stagger-3">
      <text class="footer-text">选择后可随时切换</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();
const selectedRole = ref("");

async function confirmRole() {
  if (!selectedRole.value) return;
  try {
    await userStore.setRole(selectedRole.value);
    uni.reLaunch({ url: "/pages/index/index" });
  } catch (e) {
    uni.showToast({ title: "设置失败", icon: "none" });
  }
}
</script>

<style lang="scss" scoped>
.role-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #FBF7F2;
  position: relative;
  overflow: hidden;
}

// ── 氛围背景 ──
.ambient-bg {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  pointer-events: none;
  z-index: 0;
}

.ambient-circle {
  position: absolute;
  border-radius: 50%;
}

.ambient-1 {
  width: 40%;
  height: 40%;
  top: -10%;
  left: -10%;
  background: rgba(199, 92, 58, 0.05);
  filter: blur(120rpx);
}

.ambient-2 {
  width: 30%;
  height: 30%;
  bottom: -5%;
  right: -5%;
  background: rgba(138, 154, 139, 0.05);
  filter: blur(100rpx);
}

// ── 内容 ──
.role-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 160rpx 48rpx 0;
  position: relative;
  z-index: 1;
  max-width: 600rpx;
  margin: 0 auto;
  width: 100%;
}

.hero-section {
  text-align: center;
  margin-bottom: 64rpx;
}

.hero-title {
  font-size: 96rpx;
  font-weight: $fw-bold;
  color: #C75C3A;
  letter-spacing: 2rpx;
}

// ── 角色卡片 ──
.role-cards {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.role-card {
  background: #FFFFFF;
  padding: 48rpx 32rpx;
  border-radius: 32rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0 2rpx 8rpx rgba(44, 40, 37, 0.04);
  border: 4rpx solid transparent;
  transition: all 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
  &:active {
    transform: scale(0.97);
  }
}

.role-card-active {
  border-color: #C75C3A;
  transform: scale(1.02);
  box-shadow: 0 12rpx 40rpx rgba(199, 92, 58, 0.12);
}

.role-card-icon {
  width: 96rpx;
  height: 96rpx;
  margin-bottom: 16rpx;
}

.role-card-title {
  font-size: 40rpx;
  font-weight: $fw-bold;
  color: #2C2825;
  display: block;
  margin-bottom: 8rpx;
}

.role-card-desc {
  font-size: 28rpx;
  color: #7A746E;
  line-height: $lh-relaxed;
  display: block;
  max-width: 400rpx;
}

// ── 确认按钮 ──
.confirm-area {
  margin-top: 64rpx;
  width: 100%;
  opacity: 0;
  transform: translateY(16rpx);
  transition: all 500ms $ease-out;
  pointer-events: none;
}

.confirm-area.visible {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}

.confirm-btn {
  width: 100%;
  background: #C75C3A;
  border-radius: $r-full;
  padding: 32rpx 0;
  border: none;
  box-shadow: 0 8rpx 32rpx rgba(199, 92, 58, 0.20);
  transition: all $duration-normal $ease-out;
  &:active {
    transform: scale(0.95);
  }
  &::after { border: none; }
}

.confirm-btn-text {
  font-size: 34rpx;
  font-weight: $fw-medium;
  color: #FFFFFF;
  letter-spacing: 4rpx;
}

// ── Footer ──
.role-footer {
  padding: 48rpx;
  text-align: center;
  position: relative;
  z-index: 1;
}

.footer-text {
  font-size: 28rpx;
  color: #D5CCC2;
  letter-spacing: 4rpx;
}
</style>
