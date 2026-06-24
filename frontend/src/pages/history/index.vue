<template>
  <view class="page">
    <view v-if="momentStore.loading" class="loading-center fade-in">
      <view class="loading-dot-wrap">
        <view class="loading-dot" />
        <view class="loading-dot" />
        <view class="loading-dot" />
      </view>
    </view>

    <view v-else-if="momentStore.moments.length === 0" class="empty-state fade-in">
      <view class="empty-icon-wrap">
        <text class="empty-icon">📝</text>
      </view>
      <text class="empty-title">第一份牵挂从这里开始</text>
      <text class="empty-desc">一句简单的问候，也能让家人感到温暖</text>
      <view class="btn-primary empty-btn" @tap="goSend">发送第一条</view>
    </view>

    <view v-else class="moment-list">
      <view
        v-for="(m, index) in momentStore.moments"
        :key="m.id"
        class="moment-item fade-in"
        :class="'stagger-' + Math.min(index + 1, 4)"
      >
        <view class="moment-header">
          <text class="elder-label">{{ m.elder_label || '家人' }}</text>
          <view :class="m.is_read ? 'badge-safe' : 'badge-warn'">
            <text>{{ m.is_read ? '已读' : '未读' }}</text>
          </view>
        </view>
        <view v-if="m.content_type === 'poster' && m.media_urls?.length" class="poster-thumb-row">
          <image :src="getFullUrl(m.media_urls[0])" mode="aspectFill" class="poster-thumb" />
          <text class="poster-tag">海报</text>
        </view>
        <text v-else class="moment-content">{{ m.text_content }}</text>
        <text class="moment-time">{{ m.created_at_text }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { onShow } from "@dcloudio/uni-app";
import { useMomentStore } from "@/stores/moment";
import { formatRelativeTime } from "@/utils/date";

const BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8001"
    : "https://yuxilab.cn/ezlove";

function getFullUrl(url) {
  if (!url) return "";
  if (url.startsWith("http")) return url;
  return `${BASE_URL}${url}`;
}

const momentStore = useMomentStore();

function formatTime(isoStr) {
  return formatRelativeTime(isoStr);
}

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

.loading-dot-wrap {
  display: flex;
  gap: $sp-12;
}

.loading-dot {
  width: 16rpx;
  height: 16rpx;
  border-radius: 50%;
  background: $c-primary;
  animation: dotPulse 1.2s ease-in-out infinite;
  &:nth-child(2) { animation-delay: 200ms; }
  &:nth-child(3) { animation-delay: 400ms; }
}

@keyframes dotPulse {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1.2); }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 200rpx;
}

.empty-icon-wrap {
  width: 120rpx;
  height: 120rpx;
  background: $c-primary-bg;
  border-radius: $r-2xl;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: $sp-24;
}

.empty-icon {
  font-size: 56rpx;
}

.empty-title {
  font-size: $fs-subtitle;
  font-weight: $fw-semibold;
  color: $c-text;
  display: block;
}

.empty-desc {
  font-size: $fs-body;
  color: $c-text-sub;
  margin-top: $sp-8;
  display: block;
}

.empty-btn {
  margin-top: $sp-32;
  padding: $sp-16 $sp-48;
}

.moment-item {
  background: $c-surface;
  border-radius: $r-lg;
  padding: $sp-24;
  margin-bottom: $sp-16;
  box-shadow: $shadow-sm;
  border: 1rpx solid $c-border-light;
}

.moment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $sp-12;
}

.elder-label {
  font-size: $fs-body;
  font-weight: $fw-semibold;
  color: $c-text;
}

.moment-content {
  font-size: $fs-body;
  line-height: $lh-normal;
  color: $c-text;
  display: block;
}

.moment-time {
  font-size: $fs-caption;
  color: $c-text-hint;
  margin-top: $sp-12;
  display: block;
}

.poster-thumb-row {
  display: flex;
  align-items: center;
  gap: $sp-12;
}

.poster-thumb {
  width: 120rpx;
  height: 160rpx;
  border-radius: $r-md;
  box-shadow: $shadow-xs;
}

.poster-tag {
  font-size: $fs-body-sm;
  color: $c-primary;
  background: $c-primary-bg;
  padding: $sp-4 $sp-12;
  border-radius: $r-full;
  font-weight: $fw-medium;
}
</style>
