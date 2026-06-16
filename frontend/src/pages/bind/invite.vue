<template>
  <view class="page">
    <view class="card invite-card">
      <text class="title">邀请家人加入</text>
      <text class="desc">把邀请码发给你的家人，帮Ta完成绑定</text>

      <view v-if="inviteCode" class="code-area">
        <text class="code">{{ inviteCode }}</text>
        <view class="btn-primary" @tap="copyCode">复制邀请码</view>
      </view>
      <view v-else>
        <view class="btn-primary" @tap="generate">生成邀请码</view>
      </view>
    </view>

    <view class="card bind-card" style="margin-top: 32rpx;">
      <text class="title">我有邀请码</text>
      <input v-model="inputCode" placeholder="输入邀请码" class="code-input" />
      <view class="btn-primary" @tap="handleBind">绑定</view>
    </view>
  </view>
</template>

<script setup>
import { ref } from "vue";
import { useRelationStore } from "@/stores/relation";

const relationStore = useRelationStore();
const inviteCode = ref("");
const inputCode = ref("");

async function generate() {
  try {
    const res = await relationStore.generateInvite();
    inviteCode.value = res.invite_code;
  } catch (e) {
    uni.showToast({ title: "生成失败", icon: "none" });
  }
}

function copyCode() {
  uni.setClipboardData({ data: inviteCode.value });
}

async function handleBind() {
  if (!inputCode.value) {
    uni.showToast({ title: "请输入邀请码", icon: "none" });
    return;
  }
  try {
    await relationStore.bind(inputCode.value);
    uni.showToast({ title: "绑定成功", icon: "success" });
    setTimeout(() => uni.navigateBack(), 1500);
  } catch (e) {
    uni.showToast({ title: e.message, icon: "none" });
  }
}
</script>

<style lang="scss" scoped>
.invite-card, .bind-card {
  text-align: center;
}
.title {
  font-size: $fs-title;
  font-weight: $fw-bold;
  display: block;
  margin-bottom: $sp-8;
}
.desc {
  font-size: $fs-body;
  color: $c-text-sub;
  display: block;
  margin-bottom: $sp-24;
}
.code-area {
  margin-top: $sp-24;
}
.code {
  font-size: $fs-display;
  font-weight: $fw-bold;
  color: $c-primary;
  letter-spacing: 16rpx;
  display: block;
  margin-bottom: $sp-24;
}
.code-input {
  text-align: center;
  font-size: $fs-title;
  letter-spacing: 8rpx;
  padding: $sp-16;
  background: $c-bg;
  border-radius: $r-md;
  margin-bottom: $sp-24;
}
</style>
