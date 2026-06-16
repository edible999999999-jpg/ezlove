<template>
  <view class="login-page">
    <view class="brand">
      <text class="logo-text">易挂念</text>
      <text class="slogan">让关心自然流动，让牵挂被看见</text>
    </view>

    <view class="login-actions">
      <button class="btn-wx" open-type="getUserInfo" @tap="handleLogin">
        微信一键登录
      </button>
    </view>
  </view>
</template>

<script setup>
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();

async function handleLogin() {
  try {
    uni.showLoading({ title: "登录中..." });
    await userStore.login();
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
  justify-content: center;
  align-items: center;
  padding: $sp-48;
  background: linear-gradient(180deg, $c-primary-bg 0%, $c-bg 100%);
}
.brand {
  text-align: center;
  margin-bottom: 120rpx;
}
.logo-text {
  font-size: 80rpx;
  font-weight: $fw-bold;
  color: $c-primary;
  display: block;
}
.slogan {
  font-size: $fs-body;
  color: $c-text-sub;
  margin-top: $sp-16;
}
.btn-wx {
  width: 560rpx;
  height: 96rpx;
  background: $c-primary;
  color: #FFFFFF;
  border-radius: $r-full;
  font-size: $fs-subtitle;
  font-weight: $fw-semibold;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  &::after {
    border: none;
  }
}
</style>
