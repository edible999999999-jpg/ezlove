<template>
  <view class="page-gradient">
    <view class="home-content">
      <view class="home-header fade-in" :class="{ 'elder-mode': userStore.isElder }">
        <text class="greeting">{{ greeting }}，</text>
        <text class="greeting-sub">{{ userStore.isFamily ? '今日牵挂状态' : '看看孩子们的分享' }}</text>
      </view>

      <!-- 子女端：绑定家人列表 -->
      <view v-if="userStore.isFamily" class="elder-section">
        <view v-if="relationStore.relations.length === 0" class="empty-state fade-in stagger-1">
          <view class="empty-icon-wrap">
            <text class="empty-icon">🔗</text>
          </view>
          <text class="empty-title">思念需要一个出口</text>
          <text class="empty-desc">邀请家人加入，让关心不再只放在心里</text>
          <view class="btn-primary empty-btn" @tap="goInvite">邀请家人</view>
        </view>

        <view v-else class="elder-list">
          <view
            v-for="(elder, index) in relationStore.relations"
            :key="elder.id"
            class="elder-card fade-in"
            :class="'stagger-' + Math.min(index + 1, 4)"
            @tap="goElderStatus(elder)"
          >
            <view class="elder-card-top">
              <view class="elder-avatar">
                <text class="avatar-text">{{ (elder.relation_label || '家')[0] }}</text>
              </view>
              <view class="elder-meta">
                <text class="elder-name">{{ elder.relation_label || '家人' }}</text>
                <text class="elder-last-active">{{ elder.last_active_text || '暂无活跃记录' }}</text>
              </view>
              <view class="elder-status" :class="elder.today_read ? 'badge-safe' : 'badge-warn'">
                <text>{{ elder.today_read ? '已读' : '未读' }}</text>
              </view>
            </view>
          </view>
        </view>

        <view v-if="relationStore.relations.length > 0" class="send-area fade-in stagger-3">
          <view class="btn-primary send-btn" @tap="goSend">
            <text>发送牵挂</text>
          </view>
        </view>
      </view>

      <!-- 老人端：查看子女发来的牵挂 -->
      <view v-else class="elder-home">
        <view v-if="momentStore.loading" class="loading-center fade-in">
          <view class="loading-dot-wrap">
            <view class="loading-dot" />
            <view class="loading-dot" />
            <view class="loading-dot" />
          </view>
        </view>

        <view v-else-if="momentStore.moments.length === 0" class="empty-state-elder fade-in stagger-1">
          <view class="empty-icon-wrap-elder">
            <text class="empty-icon-elder">☀️</text>
          </view>
          <text class="empty-title-elder">今天天气真好呀</text>
          <text class="empty-desc-elder">孩子们正在准备给您的惊喜呢，稍等一会儿~</text>
        </view>

        <view v-else class="elder-moment-list">
          <view
            v-for="(m, index) in momentStore.moments"
            :key="m.id"
            class="elder-moment-card fade-in"
            :class="'stagger-' + Math.min(index + 1, 4)"
            @tap="goViewDetail(m)"
          >
            <text class="elder-moment-sender">{{ m.sender_name || '家人' }} 发来的</text>
            <view v-if="m.content_type === 'poster' && m.media_urls?.length" class="elder-poster-thumb">
              <image :src="getFullUrl(m.media_urls[0])" mode="aspectFill" class="thumb-img" />
              <text class="thumb-label">海报</text>
            </view>
            <text v-else class="elder-moment-text">{{ m.text_content || '发了一张图片' }}</text>
            <view class="elder-moment-footer">
              <text class="elder-moment-time">{{ m.created_at_text || '' }}</text>
              <text class="elder-moment-action">点击查看 ›</text>
            </view>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed } from "vue";
import { onShow } from "@dcloudio/uni-app";
import { useUserStore } from "@/stores/user";
import { useRelationStore } from "@/stores/relation";
import { useMomentStore } from "@/stores/moment";

const BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8001"
    : "https://yuxilab.cn/ezlove";

function getFullUrl(url) {
  if (!url) return "";
  if (url.startsWith("http")) return url;
  return `${BASE_URL}${url}`;
}

const userStore = useUserStore();
const relationStore = useRelationStore();
const momentStore = useMomentStore();

const greeting = computed(() => {
  const hour = new Date().getHours();
  if (hour < 12) return "早上好";
  if (hour < 18) return "下午好";
  return "晚上好";
});

onShow(() => {
  if (userStore.isFamily) {
    relationStore.loadRelations();
  } else {
    momentStore.loadMoments();
  }
});

function goSend() {
  uni.navigateTo({ url: "/pages/send/index" });
}

function goElderStatus(elder) {
  uni.navigateTo({ url: `/pages/elder/status?id=${elder.elder_user_id}` });
}

function goInvite() {
  uni.navigateTo({ url: "/pages/bind/invite" });
}

function goViewDetail(m) {
  uni.navigateTo({ url: `/pages/view/detail?id=${m.id}` });
}
</script>

<style lang="scss" scoped>
.home-content {
  padding: 0 $sp-24;
  padding-bottom: 200rpx;
}

.home-header {
  padding-top: 120rpx;
  margin-bottom: $sp-40;
}

.greeting {
  font-size: $fs-headline;
  font-weight: $fw-bold;
  color: $c-text;
  display: block;
}

.greeting-sub {
  font-size: $fs-body;
  color: $c-text-sub;
  margin-top: $sp-8;
  display: block;
}

/* ── 子女端样式 ── */

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: $sp-64 $sp-24;
  background: $c-surface;
  border-radius: $r-xl;
  box-shadow: $shadow-sm;
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

.elder-card {
  background: $c-surface;
  border-radius: $r-lg;
  padding: $sp-24;
  margin-bottom: $sp-16;
  box-shadow: $shadow-sm;
  border: 1rpx solid $c-border-light;
  transition: all $duration-normal $ease-out;
  &:active {
    transform: scale(0.98);
    box-shadow: $shadow-xs;
  }
}

.elder-card-top {
  display: flex;
  align-items: center;
}

.elder-avatar {
  width: 88rpx;
  height: 88rpx;
  background: $gradient-warm-soft;
  border-radius: $r-xl;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: $sp-16;
  flex-shrink: 0;
}

.avatar-text {
  font-size: $fs-title;
  font-weight: $fw-bold;
  color: $c-primary;
}

.elder-meta {
  flex: 1;
  min-width: 0;
}

.elder-name {
  font-size: $fs-subtitle;
  font-weight: $fw-semibold;
  color: $c-text;
  display: block;
}

.elder-last-active {
  font-size: $fs-body-sm;
  color: $c-text-hint;
  margin-top: $sp-4;
  display: block;
}

.elder-status {
  flex-shrink: 0;
  margin-left: $sp-12;
}

.send-area {
  margin-top: $sp-16;
}

.send-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 104rpx;
}

.home-header.elder-mode {
  .greeting {
    font-size: $fs-elder-headline;
  }
  .greeting-sub {
    font-size: $fs-elder-body;
    margin-top: $sp-12;
  }
}

/* ── 老人端样式（大字体） ── */

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
  width: 20rpx;
  height: 20rpx;
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

.empty-state-elder {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 200rpx;
}

.empty-icon-wrap-elder {
  width: 200rpx;
  height: 200rpx;
  background: $c-primary-bg;
  border-radius: $r-2xl;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: $sp-32;
}

.empty-icon-elder {
  font-size: 100rpx;
}

.empty-title-elder {
  font-size: $fs-elder-headline;
  font-weight: $fw-bold;
  color: $c-text;
  display: block;
}

.empty-desc-elder {
  font-size: $fs-elder-body;
  color: $c-text-sub;
  margin-top: $sp-12;
  display: block;
}

.elder-moment-card {
  background: $c-surface;
  border-radius: $r-xl;
  padding: $sp-48 $sp-40;
  margin-bottom: $sp-32;
  box-shadow: $shadow-sm;
  border: 1rpx solid $c-border-light;
  transition: all $duration-normal $ease-out;
  &:active {
    transform: scale(0.98);
    background: $c-surface-warm;
  }
}

.elder-moment-sender {
  font-size: $fs-elder-title;
  color: $c-primary;
  font-weight: $fw-bold;
  display: block;
  margin-bottom: $sp-16;
}

.elder-moment-text {
  font-size: $fs-elder-title;
  line-height: $lh-relaxed;
  color: $c-text;
  display: block;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.elder-moment-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: $sp-32;
}

.elder-moment-time {
  font-size: $fs-elder-body;
  color: $c-text-hint;
}

.elder-moment-action {
  font-size: $fs-elder-title;
  color: $c-primary;
  font-weight: $fw-bold;
}

.elder-poster-thumb {
  display: flex;
  align-items: center;
  gap: $sp-16;
  margin-bottom: $sp-8;
}

.thumb-img {
  width: 200rpx;
  height: 260rpx;
  border-radius: $r-lg;
  box-shadow: $shadow-sm;
}

.thumb-label {
  font-size: $fs-elder-body;
  color: $c-text-sub;
  background: $c-primary-bg;
  padding: $sp-4 $sp-16;
  border-radius: $r-full;
}
</style>
