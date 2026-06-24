<template>
  <view class="role-page">
    <view class="role-header fade-in">
      <text class="role-title">你的身份是</text>
      <text class="role-subtitle">选择后即可开始</text>
    </view>

    <view class="role-cards">
      <view class="role-card fade-in stagger-1" @tap="selectRole('family')">
        <view class="role-card-inner">
          <view class="role-icon-wrap family">
            <text class="role-emoji">👨‍👩‍👧</text>
          </view>
          <text class="role-name">子女 / 亲属</text>
          <text class="role-desc">给父母发送每日牵挂</text>
          <view class="role-arrow">
            <text class="arrow-text">开始 →</text>
          </view>
        </view>
      </view>

      <view class="role-card fade-in stagger-2" @tap="selectRole('elder')">
        <view class="role-card-inner">
          <view class="role-icon-wrap elder">
            <text class="role-emoji">🧓</text>
          </view>
          <text class="role-name">长辈</text>
          <text class="role-desc">接收孩子的每日分享</text>
          <view class="role-arrow">
            <text class="arrow-text">开始 →</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();

async function selectRole(role) {
  try {
    await userStore.setRole(role);
    uni.reLaunch({ url: "/pages/index/index" });
  } catch (e) {
    uni.showToast({ title: "设置失败", icon: "none" });
  }
}
</script>

<style lang="scss" scoped>
.role-page {
  min-height: 100vh;
  padding: $sp-48;
  background: $gradient-hero;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.role-header {
  text-align: center;
  margin-bottom: $sp-64;
}

.role-title {
  font-size: $fs-headline;
  font-weight: $fw-bold;
  color: $c-text;
  display: block;
  letter-spacing: 4rpx;
}

.role-subtitle {
  font-size: $fs-body;
  color: $c-text-hint;
  margin-top: $sp-12;
  display: block;
}

.role-cards {
  display: flex;
  flex-direction: column;
  gap: $sp-24;
}

.role-card {
  background: $c-surface;
  border-radius: $r-xl;
  box-shadow: $shadow-md;
  overflow: hidden;
  transition: all $duration-normal $ease-out;
  &:active {
    transform: scale(0.97);
    box-shadow: $shadow-sm;
  }
}

.role-card-inner {
  padding: $sp-40 $sp-32;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.role-icon-wrap {
  width: 140rpx;
  height: 140rpx;
  border-radius: $r-2xl;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: $sp-24;
  &.family { background: $c-primary-bg; }
  &.elder { background: $c-accent-bg; }
}

.role-emoji {
  font-size: 72rpx;
}

.role-name {
  font-size: $fs-title;
  font-weight: $fw-bold;
  color: $c-text;
  display: block;
}

.role-desc {
  font-size: $fs-body;
  color: $c-text-sub;
  margin-top: $sp-8;
  display: block;
}

.role-arrow {
  margin-top: $sp-24;
  padding: $sp-8 $sp-24;
  background: $c-primary-bg;
  border-radius: $r-full;
}

.arrow-text {
  font-size: $fs-body-sm;
  color: $c-primary;
  font-weight: $fw-semibold;
}
</style>
