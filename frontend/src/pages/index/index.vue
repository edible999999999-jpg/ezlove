<template>
  <view class="page-home">
    <!-- 顶部导航栏 -->
    <view class="top-bar">
      <view class="top-bar__left">
        <view class="top-bar__avatar">
          <text class="top-bar__avatar-text">{{ (userStore.profile?.nickname || '我')[0] }}</text>
        </view>
        <text class="top-bar__greeting">你好，{{ userStore.profile?.nickname || '家人' }}</text>
      </view>
      <view class="top-bar__bell" @tap="goAlerts">
        <image class="top-bar__bell-icon" src="/static/icons/notification.svg" mode="aspectFit" />
      </view>
    </view>

    <view class="home-content">
      <!-- 大字问候区域 -->
      <view class="greeting-section fade-in">
        <text class="greeting-title" :class="{ 'greeting-title--elder': userStore.isElder }">{{ greeting }}</text>
        <view class="greeting-sub-row">
          <text class="greeting-sub" :class="{ 'greeting-sub--elder': userStore.isElder }">
            {{ userStore.isFamily ? '今日牵挂状态' : '看看孩子们的分享' }}
          </text>
          <view class="pulse-dot"></view>
        </view>
      </view>

      <!-- 子女端：绑定家人列表 -->
      <view v-if="userStore.isFamily" class="elder-section">
        <view v-if="relationStore.relations.length === 0" class="empty-state fade-in stagger-1">
          <view class="empty-icon-wrap">
            <image class="empty-icon" src="/static/icons/link.svg" mode="aspectFit" />
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
            <view class="elder-card__left">
              <view
                class="elder-card__avatar"
                :class="elder.today_read ? 'elder-card__avatar--read' : 'elder-card__avatar--unread'"
              >
                <text class="elder-card__avatar-text" :class="elder.today_read ? 'text--read' : 'text--unread'">
                  {{ (elder.relation_label || '家')[0] }}
                </text>
              </view>
              <view class="elder-card__info">
                <view class="elder-card__name-row">
                  <text class="elder-card__name">{{ elder.relation_label || '家人' }}</text>
                  <view
                    class="elder-card__badge"
                    :class="elder.today_read ? 'elder-card__badge--read' : 'elder-card__badge--unread'"
                  >
                    <text>{{ elder.today_read ? '今日已读' : '今日未读' }}</text>
                  </view>
                </view>
                <text class="elder-card__time">{{ elder.last_active_text || '暂无活跃记录' }}</text>
              </view>
            </view>
            <image class="elder-card__chevron" src="/static/icons/chevron-right.svg" mode="aspectFit" />
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
            <image class="empty-icon-elder" src="/static/icons/sun.svg" mode="aspectFit" />
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
            <view class="elder-moment-card__left">
              <view class="elder-moment-card__avatar">
                <text class="elder-moment-card__avatar-text">{{ (m.sender_name || '家')[0] }}</text>
              </view>
              <view class="elder-moment-card__info">
                <view class="elder-moment-card__name-row">
                  <text class="elder-moment-card__name">{{ m.sender_name || '家人' }}</text>
                  <view class="elder-moment-card__badge">
                    <text>发来牵挂</text>
                  </view>
                </view>
                <text class="elder-moment-card__time">{{ m.created_at_text || '' }}</text>
              </view>
            </view>
            <image class="elder-moment-card__chevron" src="/static/icons/chevron-right.svg" mode="aspectFit" />
          </view>
        </view>
      </view>
    </view>

    <!-- 底部装饰线 -->
    <view v-if="userStore.isFamily && relationStore.relations.length > 0" class="deco-line-wrap fade-in stagger-4">
      <view class="deco-line"></view>
    </view>

    <!-- FAB 浮动按钮 -->
    <view v-if="userStore.isFamily && relationStore.relations.length > 0" class="fab fade-in stagger-3" @tap="goSend">
      <image class="fab__icon" src="/static/icons/heart-send.svg" mode="aspectFit" />
      <text class="fab__text">发送牵挂</text>
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

function goAlerts() {
  uni.navigateTo({ url: "/pages/alerts/index" });
}
</script>

<style lang="scss" scoped>
// ── 页面背景 ──
.page-home {
  min-height: 100vh;
  background-color: #FBF7F2;
}

// ── 顶部导航栏 ──
.top-bar {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 50;
  background: rgba(250, 246, 241, 0.85);
  backdrop-filter: blur(24rpx);
  -webkit-backdrop-filter: blur(24rpx);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $sp-16 $sp-24;
  padding-top: calc(var(--status-bar-height, 50rpx) + #{$sp-16});
  box-sizing: border-box;

  &__left {
    display: flex;
    align-items: center;
    gap: $sp-12;
  }

  &__avatar {
    width: 80rpx;
    height: 80rpx;
    border-radius: $r-full;
    background: $c-bg-warm;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    flex-shrink: 0;
  }

  &__avatar-text {
    font-size: $fs-body;
    font-weight: $fw-bold;
    color: $c-primary;
  }

  &__greeting {
    font-size: $fs-body;
    font-weight: $fw-medium;
    color: $c-primary;
  }

  &__bell {
    padding: $sp-8;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  &__bell-icon {
    width: 44rpx;
    height: 44rpx;
  }
}

// ── 主内容区 ──
.home-content {
  // 顶部留出 top-bar 高度
  padding-top: calc(var(--status-bar-height, 50rpx) + 140rpx);
  padding-left: $sp-24;
  padding-right: $sp-24;
  padding-bottom: 260rpx;
}

// ── 问候区域 ──
.greeting-section {
  margin-bottom: $sp-40;
  background: $gradient-warm-soft;
  border-radius: $r-xl;
  padding: $sp-24 $sp-24 $sp-20;
}

.greeting-title {
  font-size: 72rpx;
  font-weight: $fw-bold;
  color: $c-text;
  display: block;
  margin-bottom: $sp-8;
  letter-spacing: -2rpx;

  &--elder {
    font-size: $fs-elder-headline;
  }
}

.greeting-sub-row {
  display: flex;
  align-items: center;
  gap: $sp-8;
}

.greeting-sub {
  font-size: 36rpx;
  color: $c-text-sub;
  opacity: 0.75;

  &--elder {
    font-size: $fs-elder-body;
  }
}

.pulse-dot {
  width: 12rpx;
  height: 12rpx;
  border-radius: $r-full;
  background-color: $c-primary;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

// ── 子女端：空状态 ──
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: $sp-64 $sp-24;
  background: $c-surface;
  border-radius: $r-lg;
  box-shadow: $shadow-sm;
}

.empty-icon-wrap {
  width: 120rpx;
  height: 120rpx;
  background: $c-primary-bg;
  border-radius: $r-full;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: $sp-24;
}

.empty-icon {
  width: 56rpx;
  height: 56rpx;
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

// ── 子女端：长辈卡片列表 ──
.elder-list {
  display: flex;
  flex-direction: column;
  gap: $sp-24;
}

.elder-card {
  background: $c-surface;
  border-radius: $r-lg;
  padding: $sp-20 $sp-20;
  box-shadow: $shadow-sm;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: all $duration-normal $ease-out;

  &:active {
    transform: scale(0.98);
    background: $c-surface-warm;
    box-shadow: $shadow-xs;
  }

  &__left {
    display: flex;
    align-items: center;
    gap: $sp-16;
    flex: 1;
    min-width: 0;
  }

  &__avatar {
    width: 112rpx;
    height: 112rpx;
    border-radius: $r-full;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;

    &--unread {
      background-color: $c-warn-bg;
    }

    &--read {
      background-color: $c-safe-bg;
    }
  }

  &__avatar-text {
    font-size: 42rpx;
    font-weight: $fw-bold;
  }

  &__info {
    flex: 1;
    min-width: 0;
  }

  &__name-row {
    display: flex;
    align-items: center;
    gap: $sp-8;
    margin-bottom: $sp-4;
  }

  &__name {
    font-size: 36rpx;
    font-weight: $fw-bold;
    color: $c-text;
  }

  &__badge {
    padding: $sp-2 $sp-10;
    border-radius: $r-full;
    font-size: $fs-caption;
    font-weight: $fw-medium;

    &--unread {
      background-color: $c-warn-bg;
      color: $c-warn;
    }

    &--read {
      background-color: $c-safe-bg;
      color: $c-safe;
    }
  }

  &__time {
    font-size: $fs-body-sm;
    color: $c-text-sub;
    display: block;
  }

  &__chevron {
    width: 36rpx;
    height: 36rpx;
    flex-shrink: 0;
    margin-left: $sp-8;
    opacity: 0.4;
  }
}

// 未读/已读文字颜色
.text--unread {
  color: $c-warn;
}

.text--read {
  color: $c-safe;
}

// ── 老人端样式（大字体）──
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
  border-radius: $r-full;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: $sp-32;
  box-shadow: $shadow-sm;
}

.empty-icon-elder {
  width: 100rpx;
  height: 100rpx;
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

// ── 老人端：牵挂卡片（与子女端统一风格）──
.elder-moment-list {
  display: flex;
  flex-direction: column;
  gap: $sp-24;
}

.elder-moment-card {
  background: $c-surface;
  border-radius: $r-lg;
  padding: $sp-24 $sp-20;
  box-shadow: $shadow-sm;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: transform $duration-normal $ease-out;

  &:active {
    transform: scale(0.98);
  }

  &__left {
    display: flex;
    align-items: center;
    gap: $sp-16;
    flex: 1;
    min-width: 0;
  }

  &__avatar {
    width: 128rpx;
    height: 128rpx;
    border-radius: $r-full;
    background-color: $c-primary-bg;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  &__avatar-text {
    font-size: $fs-elder-body;
    font-weight: $fw-bold;
    color: $c-primary;
  }

  &__info {
    flex: 1;
    min-width: 0;
  }

  &__name-row {
    display: flex;
    align-items: center;
    gap: $sp-8;
    margin-bottom: $sp-6;
  }

  &__name {
    font-size: $fs-elder-title;
    font-weight: $fw-bold;
    color: $c-text;
  }

  &__badge {
    padding: $sp-4 $sp-12;
    border-radius: $r-full;
    font-size: $fs-body;
    font-weight: $fw-medium;
    background-color: $c-accent-bg;
    color: $c-accent;
  }

  &__time {
    font-size: $fs-elder-body;
    color: $c-text-sub;
    display: block;
  }

  &__chevron {
    width: 44rpx;
    height: 44rpx;
    flex-shrink: 0;
    margin-left: $sp-8;
    opacity: 0.4;
  }
}

// ── 底部装饰线 ──
.deco-line-wrap {
  display: flex;
  justify-content: center;
  margin-top: $sp-48;
}

.deco-line {
  width: 96rpx;
  height: 4rpx;
  background-color: $c-border-light;
  border-radius: $r-full;
}

// ── FAB 浮动按钮 ──
.fab {
  position: fixed;
  bottom: 180rpx;
  right: $sp-24;
  z-index: 40;
  background: $c-primary;
  color: $c-text-inverse;
  display: flex;
  align-items: center;
  gap: $sp-8;
  padding: $sp-16 $sp-24;
  border-radius: $r-full;
  box-shadow: $shadow-lg;
  transition: all $duration-normal $ease-out;
  animation: fabBounceIn 600ms $ease-spring both 400ms, fabBreath 3s ease-in-out infinite 1.2s;

  &:active {
    transform: scale(0.9);
    animation: none;
  }

  &__icon {
    width: 36rpx;
    height: 36rpx;
  }

  &__text {
    font-size: $fs-body;
    font-weight: $fw-medium;
    letter-spacing: 2rpx;
    color: $c-text-inverse;
  }
}

@keyframes fabBounceIn {
  0% { opacity: 0; transform: translateY(60rpx) scale(0.6); }
  60% { opacity: 1; transform: translateY(-8rpx) scale(1.05); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes fabBreath {
  0%, 100% { box-shadow: $shadow-lg; }
  50% { box-shadow: 0 12rpx 48rpx rgba(196, 116, 92, 0.35); }
}
</style>
