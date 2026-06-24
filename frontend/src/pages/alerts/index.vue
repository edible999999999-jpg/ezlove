<template>
  <view class="page">
    <view v-if="alertStore.alerts.length === 0" class="empty-state fade-in">
      <view class="safe-icon-wrap">
        <text class="safe-icon">🌿</text>
      </view>
      <text class="safe-title">一切安好</text>
      <text class="safe-desc">家人们都好好的，放心吧</text>
    </view>

    <view v-else class="alert-list">
      <view
        v-for="(a, index) in alertStore.alerts"
        :key="a.id"
        class="alert-item fade-in"
        :class="[{ resolved: a.is_resolved }, 'stagger-' + Math.min(index + 1, 4)]"
      >
        <view class="alert-header">
          <view class="level-badge" :class="a.alert_level">
            <text>{{ levelText(a.alert_level) }}</text>
          </view>
          <text class="alert-time">{{ a.created_at_text }}</text>
        </view>
        <text class="alert-msg">{{ a.message }}</text>
        <view v-if="!a.is_resolved" class="alert-actions">
          <view class="resolve-btn" @tap="handleResolve(a.id)">
            <text>已确认安好</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { onShow } from "@dcloudio/uni-app";
import { useAlertStore } from "@/stores/alert";

const alertStore = useAlertStore();

onShow(() => {
  alertStore.loadAlerts();
});

function levelText(level) {
  const map = { info: "提示", warning: "注意", urgent: "紧急" };
  return map[level] || level;
}

async function handleResolve(id) {
  await alertStore.resolve(id);
  uni.showToast({ title: "已标记", icon: "success" });
}
</script>

<style lang="scss" scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 240rpx;
}

.safe-icon-wrap {
  width: 140rpx;
  height: 140rpx;
  background: $c-safe-bg;
  border-radius: $r-2xl;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: $sp-24;
}

.safe-icon {
  font-size: 64rpx;
}

.safe-title {
  font-size: $fs-title;
  font-weight: $fw-bold;
  color: $c-safe;
  display: block;
}

.safe-desc {
  font-size: $fs-body;
  color: $c-text-sub;
  margin-top: $sp-8;
  display: block;
}

.alert-item {
  background: $c-surface;
  border-radius: $r-lg;
  padding: $sp-24;
  margin-bottom: $sp-16;
  box-shadow: $shadow-sm;
  border: 1rpx solid $c-border-light;
  transition: opacity $duration-normal;
  &.resolved {
    opacity: 0.5;
  }
}

.alert-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $sp-12;
}

.level-badge {
  padding: $sp-4 $sp-16;
  border-radius: $r-full;
  font-size: $fs-body-sm;
  font-weight: $fw-medium;
  &.info {
    background: $c-accent-bg;
    color: $c-accent;
  }
  &.warning {
    background: $c-warn-bg;
    color: $c-warn;
  }
  &.urgent {
    background: rgba($c-warn, 0.15);
    color: $c-warn;
    font-weight: $fw-semibold;
  }
}

.alert-time {
  font-size: $fs-caption;
  color: $c-text-hint;
}

.alert-msg {
  font-size: $fs-body;
  line-height: $lh-normal;
  color: $c-text;
  display: block;
}

.alert-actions {
  margin-top: $sp-20;
}

.resolve-btn {
  text-align: center;
  padding: $sp-12;
  border-radius: $r-full;
  border: 2rpx solid $c-safe;
  color: $c-safe;
  font-size: $fs-body;
  font-weight: $fw-medium;
  transition: all $duration-normal $ease-out;
  &:active {
    background: $c-safe-bg;
    transform: scale(0.97);
  }
}
</style>
