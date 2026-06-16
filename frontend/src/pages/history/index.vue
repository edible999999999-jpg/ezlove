<template>
  <view class="page">
    <view v-if="momentStore.loading" class="loading-center">
      <u-loading-icon mode="circle" color="#FF8C42" />
    </view>

    <view v-else-if="momentStore.moments.length === 0" class="empty">
      <text class="empty-text">还没有发送过牵挂</text>
      <view class="btn-primary" @tap="goSend">发送第一条</view>
    </view>

    <view v-else class="moment-list">
      <view v-for="m in momentStore.moments" :key="m.id" class="card moment-item">
        <view class="moment-header">
          <text class="elder-label">{{ m.elder_label || '家人' }}</text>
          <view class="status-dot" :class="m.is_read ? 'read' : 'unread'" />
          <text class="status-text" :class="m.is_read ? 'status-read' : 'status-unread'">
            {{ m.is_read ? '已读' : '未读' }}
          </text>
        </view>
        <text class="moment-content">{{ m.text_content }}</text>
        <text class="moment-time">{{ m.created_at_text }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { onShow } from "@dcloudio/uni-app";
import { useMomentStore } from "@/stores/moment";

const momentStore = useMomentStore();

onShow(() => {
  momentStore.loadMoments();
});

function goSend() {
  uni.navigateTo({ url: "/pages/send/index" });
}
</script>

<style lang="scss" scoped>
.loading-center {
  display: flex;
  justify-content: center;
  padding-top: 200rpx;
}
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 200rpx;
}
.empty-text {
  color: $c-text-hint;
  margin-bottom: $sp-24;
}
.moment-item {
  margin-bottom: $sp-16;
}
.moment-header {
  display: flex;
  align-items: center;
  gap: $sp-8;
  margin-bottom: $sp-12;
}
.elder-label {
  font-weight: $fw-semibold;
}
.status-dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  &.read { background: $c-safe; }
  &.unread { background: $c-warn; }
}
.status-text {
  font-size: $fs-body-sm;
}
.moment-content {
  font-size: $fs-body;
  line-height: 1.6;
  display: block;
}
.moment-time {
  font-size: $fs-caption;
  color: $c-text-hint;
  margin-top: $sp-8;
  display: block;
}
</style>
