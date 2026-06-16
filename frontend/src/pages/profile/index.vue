<template>
  <view class="page">
    <view class="card profile-card">
      <text class="nickname">{{ userStore.profile?.nickname || '未设置昵称' }}</text>
      <text class="role-text">{{ userStore.isFamily ? '子女/亲属' : '长辈' }}</text>
    </view>

    <view class="menu-list">
      <view class="card menu-item" @tap="goBindList">
        <text>我的家人</text>
        <text class="arrow">></text>
      </view>
      <view class="card menu-item" @tap="goInvite">
        <text>邀请绑定</text>
        <text class="arrow">></text>
      </view>
      <view class="card menu-item logout" @tap="handleLogout">
        <text>退出登录</text>
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
.profile-card {
  text-align: center;
  padding: $sp-48 $sp-24;
  margin-bottom: $sp-24;
}
.nickname {
  font-size: $fs-headline;
  font-weight: $fw-bold;
  display: block;
}
.role-text {
  font-size: $fs-body;
  color: $c-primary;
  margin-top: $sp-8;
  display: block;
}
.menu-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $sp-12;
  padding: $sp-20 $sp-24;
}
.arrow {
  color: $c-text-hint;
}
.logout {
  color: $c-warn;
  justify-content: center;
  margin-top: $sp-24;
}
</style>
