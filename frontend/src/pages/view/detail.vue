<template>
  <view class="elder-page">
    <!-- Top Bar -->
    <view class="top-bar">
      <view class="top-bar-left">
        <view class="back-btn" @tap="goBack">
          <text class="back-icon">←</text>
        </view>
        <text class="top-bar-title">牵挂</text>
      </view>
      <view class="top-bar-avatar">
        <text class="top-bar-initial">{{ (moment.elder_nickname || moment.sender_name || '我')[0] }}</text>
      </view>
    </view>

    <!-- Loading -->
    <view v-if="loading" class="loading-center">
      <view class="loading-dots">
        <view class="ld-dot" />
        <view class="ld-dot" />
        <view class="ld-dot" />
      </view>
    </view>

    <!-- Message Card -->
    <view v-if="!loading && moment.id" class="message-card card-enter">
      <!-- Sender Header -->
      <view class="sender-header">
        <view class="sender-info">
          <view class="sender-avatar-sm">
            <text class="sender-avatar-initial">{{ (moment.sender_nickname || moment.sender_name || '家')[0] }}</text>
          </view>
          <view class="sender-meta">
            <text class="sender-name">{{ moment.sender_nickname || moment.sender_name || '家人' }}</text>
            <text class="sender-time">{{ timeText }}</text>
          </view>
        </view>
        <view class="family-badge">
          <text class="family-badge-text">家人留言</text>
        </view>
      </view>

      <!-- Body Text -->
      <view class="message-body">
        <text class="body-text">{{ moment.text_content }}</text>
      </view>

      <!-- Image Content -->
      <view v-if="moment.content_type === 'poster' && moment.media_urls?.length" class="image-area">
        <image
          :src="getFullUrl(moment.media_urls[0])"
          mode="widthFix"
          class="content-image"
          @tap="previewPoster"
        />
      </view>
      <view v-else-if="moment.media_urls?.length" class="image-area">
        <image
          :src="getFullUrl(moment.media_urls[0])"
          mode="widthFix"
          class="content-image"
          @tap="previewPoster"
        />
      </view>

      <!-- Caption -->
      <text class="image-caption">— 来自家人的温馨分享 —</text>
    </view>

    <!-- Reaction Section -->
    <view v-if="!loading && moment.id" class="reaction-section reactions-enter">
      <!-- Divider with text -->
      <view class="reaction-divider">
        <view class="divider-line" />
        <text class="divider-text">让 Ta 知道你看到了</text>
        <view class="divider-line" />
      </view>

      <!-- Reaction Buttons -->
      <view class="reaction-grid">
        <view class="reaction-btn" @tap="sendReaction('like')">
          <view class="reaction-circle">
            <text class="reaction-emoji">👍</text>
          </view>
          <text class="reaction-label">点赞</text>
        </view>
        <view class="reaction-btn" @tap="sendReaction('love')">
          <view class="reaction-circle">
            <text class="reaction-emoji">❤️</text>
          </view>
          <text class="reaction-label">温暖</text>
        </view>
        <view class="reaction-btn" @tap="sendReaction('happy')">
          <view class="reaction-circle">
            <text class="reaction-emoji">😊</text>
          </view>
          <text class="reaction-label">开心</text>
        </view>
        <view class="reaction-btn" @tap="sendReaction('hug')">
          <view class="reaction-circle">
            <text class="reaction-emoji">🤗</text>
          </view>
          <text class="reaction-label">拥抱</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { getMomentDetail, recordView, sendResponse } from "@/api/moment";
import { getFullUrl } from "@/api/config";

const moment = ref({});
const momentId = ref("");
const loading = ref(true);

const timeText = computed(() => {
  if (!moment.value.created_at) return "";
  const d = new Date(moment.value.created_at);
  const now = new Date();
  const diffMs = now - d;
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return "刚刚";
  if (diffMin < 60) return `${diffMin} 分钟前`;
  const diffH = Math.floor(diffMin / 60);
  if (diffH < 24) return `${diffH} 小时前`;
  const month = (d.getMonth() + 1).toString().padStart(2, "0");
  const day = d.getDate().toString().padStart(2, "0");
  return `${month}-${day}`;
});

onLoad((query) => {
  momentId.value = query.id;
  loadMoment();
});

async function loadMoment() {
  loading.value = true;
  try {
    moment.value = await getMomentDetail(momentId.value);
    await recordView(momentId.value);
  } catch (e) {
    uni.showToast({ title: "内容加载失败", icon: "none" });
  } finally {
    loading.value = false;
  }
}

function previewPoster() {
  if (moment.value.media_urls?.length) {
    uni.previewImage({
      urls: [getFullUrl(moment.value.media_urls[0])],
    });
  }
}

function goBack() {
  uni.navigateBack({ delta: 1 });
}

async function sendReaction(type) {
  try {
    await sendResponse(momentId.value, { response_type: type });
    uni.showToast({ title: "已发送", icon: "success" });
  } catch {
    uni.showToast({ title: "发送失败", icon: "none" });
  }
}
</script>

<style lang="scss" scoped>
.elder-page {
  min-height: 100vh;
  padding-top: calc(var(--status-bar-height, 50rpx) + 128rpx);
  padding-bottom: 200rpx;
  padding-left: $sp-24;
  padding-right: $sp-24;
  background: $c-bg;
}

/* Top Bar */
.top-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 $sp-24;
  padding-top: var(--status-bar-height, 50rpx);
  height: calc(var(--status-bar-height, 50rpx) + 112rpx);
  background: rgba(250, 246, 241, 0.9);
  backdrop-filter: blur(24rpx);
  -webkit-backdrop-filter: blur(24rpx);
}

.top-bar-left {
  display: flex;
  align-items: center;
  gap: $sp-16;
}

.back-btn {
  width: 96rpx;
  height: 96rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: $r-full;
  transition: background $duration-normal;

  &:active {
    background: $c-bg-warm;
  }
}

.back-icon {
  font-size: 60rpx;
  color: $c-text;
}

.top-bar-title {
  font-size: 48rpx;
  font-weight: $fw-bold;
  color: $c-primary;
  letter-spacing: -1rpx;
}

.top-bar-avatar {
  width: 80rpx;
  height: 80rpx;
  border-radius: $r-full;
  background: $c-primary-bg;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 4rpx solid $c-surface;
  box-shadow: $shadow-sm;
}

.top-bar-initial {
  font-size: $fs-title;
  font-weight: $fw-bold;
  color: $c-primary;
}

/* Loading */
.loading-center {
  display: flex;
  justify-content: center;
  padding-top: 200rpx;
}

.loading-dots {
  display: flex;
  gap: $sp-12;
}

.ld-dot {
  width: 20rpx;
  height: 20rpx;
  border-radius: 50%;
  background: $c-primary-soft;
  animation: ldPulse 1.2s ease-in-out infinite;
  &:nth-child(2) { animation-delay: 200ms; }
  &:nth-child(3) { animation-delay: 400ms; }
}

@keyframes ldPulse {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1.2); }
}

/* Entrance Animations */
.card-enter {
  animation: cardSlideUp 500ms $ease-out both;
}

.reactions-enter {
  animation: cardSlideUp 500ms $ease-out both;
  animation-delay: 250ms;
}

@keyframes cardSlideUp {
  0% {
    opacity: 0;
    transform: translateY(40rpx) scale(0.97);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Message Card */
.message-card {
  background: $c-surface-warm;
  border-radius: 48rpx;
  padding: $sp-32;
  margin-bottom: $sp-32;
  box-shadow: $shadow-md;
  border: $border-subtle;
}

/* Sender Header */
.sender-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $sp-24;
}

.sender-info {
  display: flex;
  align-items: center;
  gap: $sp-12;
}

.sender-avatar-sm {
  width: 80rpx;
  height: 80rpx;
  background: $c-primary-bg;
  border-radius: $r-full;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sender-avatar-initial {
  font-size: 36rpx;
  font-weight: $fw-bold;
  color: $c-primary;
}

.sender-meta {
  display: flex;
  flex-direction: column;
}

.sender-name {
  font-size: $fs-elder-body;
  font-weight: $fw-medium;
  color: $c-text-sub;
  display: block;
}

.sender-time {
  font-size: $fs-body;
  color: $c-text-hint;
  opacity: 0.75;
  display: block;
  margin-top: $sp-2;
}

.family-badge {
  padding: $sp-4 $sp-12;
  background: rgba($c-primary, 0.1);
  border-radius: $r-full;
}

.family-badge-text {
  font-size: $fs-body;
  font-weight: $fw-bold;
  color: $c-primary;
}

/* Message Body */
.message-body {
  margin-bottom: $sp-32;
}

.body-text {
  font-size: $fs-elder-body;
  line-height: $lh-relaxed;
  font-weight: $fw-medium;
  color: $c-text;
  display: block;
}

/* Image Area */
.image-area {
  width: 100%;
  border-radius: $r-xl;
  overflow: hidden;
  margin-bottom: $sp-8;
}

.content-image {
  width: 100%;
  display: block;
  border-radius: $r-xl;
}

/* Image Caption */
.image-caption {
  display: block;
  text-align: center;
  font-size: $fs-body;
  color: $c-text-hint;
  opacity: 0.6;
  font-style: italic;
  margin-top: $sp-16;
}

/* Reaction Section */
.reaction-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.reaction-divider {
  display: flex;
  align-items: center;
  gap: $sp-8;
  margin-bottom: $sp-24;
  width: 100%;
  justify-content: center;
}

.divider-line {
  width: 64rpx;
  height: 2rpx;
  background: $c-border;
}

.divider-text {
  font-size: $fs-elder-body;
  font-weight: $fw-medium;
  color: $c-text-sub;
  white-space: nowrap;
}

/* Reaction Grid */
.reaction-grid {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 560rpx;
  gap: $sp-16;
}

.reaction-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $sp-8;

  &:active .reaction-circle {
    transform: scale(0.85);
    background: $c-primary-bg;
    border-color: $c-primary;
    box-shadow: 0 0 0 8rpx rgba(196, 116, 92, 0.1);
  }
}

.reaction-circle {
  width: 128rpx;
  height: 128rpx;
  border-radius: $r-full;
  background: $c-surface;
  box-shadow: $shadow-sm;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2rpx solid rgba($c-border, 0.3);
  transition: all $duration-normal $ease-spring;
}

.reaction-emoji {
  font-size: 56rpx;
}

.reaction-label {
  font-size: $fs-body;
  font-weight: $fw-medium;
  color: $c-text-sub;
}
</style>
