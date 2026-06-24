<template>
  <view class="page-gradient">
    <view class="profile-content">
      <view class="profile-header fade-in">
        <view class="avatar-circle">
          <text class="avatar-letter">{{ (userStore.profile?.nickname || '我')[0] }}</text>
        </view>
        <text class="nickname">{{ userStore.profile?.nickname || '未设置昵称' }}</text>
        <view class="role-tag">
          <text>{{ userStore.isFamily ? '子女/亲属' : '长辈' }}</text>
        </view>
      </view>

      <view class="menu-section fade-in stagger-1">
        <view class="menu-card" @tap="goBindList">
          <view class="menu-left">
            <text class="menu-icon">👨‍👩‍👧</text>
            <text class="menu-text">我的家人</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
        <view class="menu-card" @tap="goInvite">
          <view class="menu-left">
            <text class="menu-icon">🔗</text>
            <text class="menu-text">邀请绑定</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
      </view>

      <view class="logout-section fade-in stagger-2">
        <view class="logout-btn" @tap="handleLogout">
          <text class="logout-text">退出登录</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();

function goBindList() {
  uni.navigateTo({ url: "/pages/bind/list" });
}

function goInvite() {
  uni.navigateTo({ url: "/pages/bind/invite" });
}

function handleLogout() {
  uni.showModal({
    title: "退出登录",
    content: "确定退出吗？",
    success: (res) => {
      if (res.confirm) userStore.logout();
    },
  });
}
</script>

<style lang="scss" scoped>
.profile-content {
  padding: 0 $sp-24;
  padding-bottom: 200rpx;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 120rpx;
  padding-bottom: $sp-48;
}

.avatar-circle {
  width: 160rpx;
  height: 160rpx;
  background: $gradient-warm;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 32rpx rgba(196, 116, 92, 0.25);
  margin-bottom: $sp-20;
}

.avatar-letter {
  font-size: $fs-display;
  font-weight: $fw-bold;
  color: $c-text-inverse;
}

.nickname {
  font-size: $fs-headline;
  font-weight: $fw-bold;
  color: $c-text;
  display: block;
}

.role-tag {
  margin-top: $sp-12;
  padding: $sp-6 $sp-20;
  background: $c-primary-bg;
  border-radius: $r-full;
  font-size: $fs-body-sm;
  color: $c-primary;
  font-weight: $fw-medium;
}

.menu-section {
  display: flex;
  flex-direction: column;
  gap: $sp-12;
}

.menu-card {
  background: $c-surface;
  border-radius: $r-lg;
  padding: $sp-24;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: $shadow-sm;
  border: 1rpx solid $c-border-light;
  transition: all $duration-normal $ease-out;
  &:active {
    transform: scale(0.98);
    background: $c-surface-warm;
  }
}

.menu-left {
  display: flex;
  align-items: center;
  gap: $sp-16;
}

.menu-icon {
  font-size: $fs-title;
}

.menu-text {
  font-size: $fs-body;
  font-weight: $fw-medium;
  color: $c-text;
}

.menu-arrow {
  font-size: $fs-title;
  color: $c-text-hint;
}

.logout-section {
  margin-top: $sp-48;
}

.logout-btn {
  text-align: center;
  padding: $sp-20;
  border-radius: $r-lg;
  background: $c-surface;
  border: 1rpx solid $c-border-light;
  transition: all $duration-normal $ease-out;
  &:active {
    background: $c-warn-bg;
  }
}

.logout-text {
  font-size: $fs-body;
  color: $c-warn;
  font-weight: $fw-medium;
}
</style>
