<template>
  <view class="role-page">
    <text class="title">你是</text>

    <view class="role-cards">
      <view class="card role-card" @tap="selectRole('family')">
        <text class="role-emoji">👨‍👩‍👧</text>
        <text class="role-name">子女/亲属</text>
        <text class="role-desc">我想给父母发送每日牵挂</text>
      </view>

      <view class="card role-card" @tap="selectRole('elder')">
        <text class="role-emoji">👴</text>
        <text class="role-name">长辈</text>
        <text class="role-desc">我想收到孩子的每日分享</text>
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
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.title {
  font-size: $fs-headline;
  font-weight: $fw-bold;
  text-align: center;
  margin-bottom: $sp-48;
}
.role-cards {
  display: flex;
  flex-direction: column;
  gap: $sp-24;
}
.role-card {
  text-align: center;
  padding: $sp-48 $sp-24;
  &:active {
    transform: scale(0.97);
    border-color: $c-primary;
  }
}
.role-emoji {
  font-size: 80rpx;
  display: block;
  margin-bottom: $sp-16;
}
.role-name {
  font-size: $fs-title;
  font-weight: $fw-bold;
  display: block;
}
.role-desc {
  font-size: $fs-body;
  color: $c-text-sub;
  margin-top: $sp-8;
}
</style>
