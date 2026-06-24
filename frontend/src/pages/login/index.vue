<template>
  <view class="login-page">
    <view class="hero-area fade-in">
      <view class="logo-mark">
        <text class="logo-icon">💌</text>
      </view>
      <text class="brand-name">易挂念</text>
      <text class="brand-tagline">让关心自然流动</text>
      <text class="brand-sub">让牵挂被看见</text>
    </view>

    <view class="login-bottom fade-in stagger-2">
      <button class="login-btn" @tap="handleLogin()">
        <text class="login-btn-text">微信一键登录</text>
      </button>

      <!-- H5 测试：老人端入口 -->
      <!-- #ifdef H5 -->
      <button class="login-btn-elder" @tap="handleLogin('dev_test_elder')">
        <text class="login-btn-elder-text">老人端测试入口</text>
      </button>
      <!-- #endif -->

      <text class="login-hint">登录即代表同意《用户协议》</text>
    </view>
  </view>
</template>

<script setup>
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();

async function handleLogin(openid) {
  try {
    uni.showLoading({ title: "登录中..." });
    await userStore.login(openid);
    uni.hideLoading();

    if (!userStore.hasRole) {
      uni.reLaunch({ url: "/pages/login/role" });
    } else {
      uni.reLaunch({ url: "/pages/index/index" });
    }
  } catch (e) {
    uni.hideLoading();
    uni.showToast({ title: "登录失败，请重试", icon: "none" });
  }
}
</script>

<style lang="scss" scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: $gradient-hero;
  overflow: hidden;
}

.hero-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 $sp-48;
}

.logo-mark {
  width: 160rpx;
  height: 160rpx;
  background: $c-surface;
  border-radius: $r-2xl;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: $shadow-lg;
  margin-bottom: $sp-40;
}

.logo-icon {
  font-size: 80rpx;
}

.brand-name {
  font-size: $fs-hero;
  font-weight: $fw-bold;
  color: $c-primary;
  letter-spacing: 12rpx;
  display: block;
}

.brand-tagline {
  font-size: $fs-title;
  color: $c-text;
  margin-top: $sp-16;
  font-weight: $fw-medium;
  letter-spacing: 4rpx;
}

.brand-sub {
  font-size: $fs-body;
  color: $c-text-sub;
  margin-top: $sp-8;
  letter-spacing: 2rpx;
}

.login-bottom {
  padding: $sp-48;
  padding-bottom: 120rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-btn {
  width: 100%;
  height: 104rpx;
  background: $gradient-warm;
  border-radius: $r-full;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  box-shadow: 0 8rpx 32rpx rgba(196, 116, 92, 0.3);
  transition: all $duration-normal $ease-out;
  &:active {
    transform: scale(0.97);
    box-shadow: 0 4rpx 16rpx rgba(196, 116, 92, 0.2);
  }
  &::after { border: none; }
}

.login-btn-text {
  font-size: $fs-subtitle;
  font-weight: $fw-semibold;
  color: $c-text-inverse;
  letter-spacing: 4rpx;
}

.login-btn-elder {
  width: 100%;
  height: 96rpx;
  background: $c-surface;
  border-radius: $r-full;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2rpx solid $c-primary-soft;
  margin-top: $sp-16;
  transition: all $duration-normal $ease-out;
  &:active {
    transform: scale(0.97);
    background: $c-primary-bg;
  }
  &::after { border: none; }
}

.login-btn-elder-text {
  font-size: $fs-body;
  font-weight: $fw-medium;
  color: $c-primary;
  letter-spacing: 2rpx;
}

.login-hint {
  font-size: $fs-caption;
  color: $c-text-hint;
  margin-top: $sp-20;
}
</style>
