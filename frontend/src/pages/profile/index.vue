<template>
  <view class="page-gradient">
    <view class="profile-content">
      <view class="profile-header fade-in">
        <view class="avatar-circle">
          <text class="avatar-letter">{{ (userStore.profile?.nickname || '我')[0] }}</text>
        </view>
        <text class="nickname">{{ userStore.profile?.nickname || '未设置昵称' }}</text>
        <view class="role-tag">
          <text>{{ userStore.isFamily ? '子女/亲属' : '长辈' }}</text>
        </view>
        <text class="greeting-text">{{ greeting }}</text>
      </view>

      <view v-if="userStore.isFamily && statsLoaded" class="stats-row fade-in stagger-1">
        <view class="stat-item">
          <text class="stat-num">{{ elderCount }}</text>
          <text class="stat-label">守护家人</text>
        </view>
        <view class="stat-divider" />
        <view class="stat-item">
          <text class="stat-num">{{ momentCount }}</text>
          <text class="stat-label">牵挂已送</text>
        </view>
        <view class="stat-divider" />
        <view class="stat-item">
          <text class="stat-num">{{ careStreak }}</text>
          <text class="stat-label">连续天数</text>
        </view>
      </view>

      <view class="menu-section fade-in stagger-2">
        <template v-if="userStore.isFamily">
          <view class="menu-card" @tap="goBindList">
            <view class="menu-left">
              <image class="menu-icon-img" src="/static/icons/family.svg" mode="aspectFit" />
              <text class="menu-text">我的家人</text>
            </view>
            <text class="menu-arrow">›</text>
          </view>
          <view class="menu-card" @tap="goInvite">
            <view class="menu-left">
              <image class="menu-icon-img" src="/static/icons/link.svg" mode="aspectFit" />
              <text class="menu-text">邀请绑定</text>
            </view>
            <text class="menu-arrow">›</text>
          </view>
        </template>
        <view class="menu-card" @tap="goVolunteer">
          <view class="menu-left">
            <image class="menu-icon-img" src="/static/icons/heart-send.svg" mode="aspectFit" />
            <text class="menu-text">邻里帮</text>
          </view>
          <text class="menu-arrow">›</text>
        </view>
      </view>

      <view class="logout-section fade-in stagger-3">
        <view class="logout-btn" @tap="handleLogout">
          <text class="logout-text">退出登录</text>
        </view>
        <text class="version-text">易挂念 v1.0.0</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from "vue";
import { onShow } from "@dcloudio/uni-app";
import { useUserStore } from "@/stores/user";
import { getRelations } from "@/api/relation";
import { getMoments } from "@/api/moment";

const userStore = useUserStore();
const elderCount = ref(0);
const momentCount = ref(0);
const careStreak = ref(0);
const statsLoaded = ref(false);

const greeting = computed(() => {
  const h = new Date().getHours();
  const name = userStore.profile?.nickname || "";
  if (h < 6) return `${name}，夜深了，注意休息`;
  if (h < 11) return `${name}，早上好`;
  if (h < 14) return `${name}，中午好`;
  if (h < 18) return `${name}，下午好`;
  return `${name}，晚上好`;
});

onShow(() => {
  if (userStore.isFamily) loadStats();
});

async function loadStats() {
  try {
    const [relations, moments] = await Promise.all([
      getRelations(),
      getMoments({ limit: 200 }),
    ]);
    elderCount.value = relations.length;
    momentCount.value = moments.length;
    careStreak.value = calcStreak(moments);
    statsLoaded.value = true;
  } catch {
    // silent
  }
}

function calcStreak(moments) {
  if (!moments.length) return 0;
  const days = new Set();
  moments.forEach((m) => {
    if (m.created_at) days.add(m.created_at.slice(0, 10));
  });
  const sorted = [...days].sort().reverse();
  const today = new Date().toISOString().slice(0, 10);
  if (sorted[0] !== today) return 0;
  let streak = 1;
  for (let i = 1; i < sorted.length; i++) {
    const prev = new Date(sorted[i - 1]);
    const cur = new Date(sorted[i]);
    const diff = (prev - cur) / 86400000;
    if (diff === 1) streak++;
    else break;
  }
  return streak;
}

function goBindList() {
  uni.navigateTo({ url: "/pages/bind/list" });
}

function goInvite() {
  uni.navigateTo({ url: "/pages/bind/invite" });
}

function goVolunteer() {
  uni.navigateTo({ url: "/pages/volunteer/index" });
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
.profile-content {
  padding: 0 $sp-24;
  padding-bottom: 200rpx;
}

.profile-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 120rpx;
  padding-bottom: $sp-48;
}

.avatar-circle {
  width: 160rpx;
  height: 160rpx;
  background: $gradient-warm;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: $shadow-glow;
  margin-bottom: $sp-20;
  border: 6rpx solid rgba(255, 255, 255, 0.8);
}

.avatar-letter {
  font-size: $fs-display;
  font-weight: $fw-bold;
  color: $c-text-inverse;
}

.nickname {
  font-size: $fs-headline;
  font-weight: $fw-bold;
  color: $c-text;
  display: block;
}

.role-tag {
  margin-top: $sp-12;
  padding: $sp-6 $sp-20;
  background: $c-primary-bg;
  border-radius: $r-full;
  font-size: $fs-body-sm;
  color: $c-primary;
  font-weight: $fw-medium;
}

.greeting-text {
  margin-top: $sp-16;
  font-size: $fs-body;
  color: $c-text-sub;
}

.stats-row {
  display: flex;
  align-items: center;
  justify-content: space-around;
  background: $c-surface;
  border-radius: $r-xl;
  padding: $sp-24 $sp-16;
  margin-bottom: $sp-20;
  box-shadow: $shadow-md;
  border: $border-subtle;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $sp-6;
}

.stat-num {
  font-size: $fs-headline;
  font-weight: $fw-bold;
  color: $c-primary;
}

.stat-label {
  font-size: $fs-body-sm;
  color: $c-text-sub;
}

.stat-divider {
  width: 1rpx;
  height: 60rpx;
  background: $c-border-light;
}

.menu-section {
  display: flex;
  flex-direction: column;
  gap: $sp-12;
}

.menu-card {
  background: $c-surface;
  border-radius: $r-lg;
  padding: $sp-32;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: $shadow-md;
  border: $border-subtle;
  border-left: 6rpx solid $c-primary-soft;
  transition: all $duration-normal $ease-out;
  &:active {
    transform: scale(0.98);
    background: $c-surface-warm;
    box-shadow: $shadow-sm;
  }
}

.menu-left {
  display: flex;
  align-items: center;
  gap: $sp-16;
}

.menu-icon-img {
  width: 48rpx;
  height: 48rpx;
}

.menu-text {
  font-size: $fs-title;
  font-weight: $fw-medium;
  color: $c-text;
}

.menu-arrow {
  font-size: $fs-title;
  color: $c-text-hint;
}

.logout-section {
  margin-top: $sp-48;
}

.logout-btn {
  text-align: center;
  padding: $sp-20;
  border-radius: $r-full;
  background: $c-surface;
  border: 2rpx solid $c-warn-soft;
  box-shadow: $shadow-sm;
  transition: all $duration-normal $ease-out;
  &:active {
    background: $c-warn-bg;
    transform: scale(0.97);
  }
}

.logout-text {
  font-size: $fs-body;
  color: $c-warn;
  font-weight: $fw-medium;
}

.version-text {
  display: block;
  text-align: center;
  margin-top: $sp-24;
  font-size: $fs-caption;
  color: $c-text-hint;
  opacity: 0.5;
}
</style>
