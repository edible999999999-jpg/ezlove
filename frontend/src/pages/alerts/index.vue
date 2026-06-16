<template>
  <view class="page">
    <view v-if="alertStore.alerts.length === 0" class="empty">
      <text class="empty-text">暂无提醒，一切安好</text>
    </view>

    <view v-else class="alert-list">
      <view
        v-for="a in alertStore.alerts"
        :key="a.id"
        class="card alert-item"
        :class="{ resolved: a.is_resolved }"
      >
        <view class="alert-header">
          <view class="level-badge" :class="a.alert_level">
            <text>{{ levelText(a.alert_level) }}</text>
          </view>
          <text class="alert-time">{{ a.created_at_text }}</text>
        </view>
        <text class="alert-msg">{{ a.message }}</text>
        <view v-if="!a.is_resolved" class="alert-actions">
          <view class="btn-resolve" @tap="handleResolve(a.id)">已确认安好</view>
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
.empty {
  display: flex;
  justify-content: center;
  padding-top: 200rpx;
}
.empty-text {
  color: $c-text-hint;
}
.alert-item {
  margin-bottom: $sp-16;
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
  padding: $sp-4 $sp-12;
  border-radius: $r-full;
  font-size: $fs-body-sm;
  &.info { background: #E3F2FD; color: #1976D2; }
  &.warning { background: $c-secondary-bg; color: #F59E0B; }
  &.urgent { background: $c-warn-bg; color: $c-warn; }
}
.alert-time {
  font-size: $fs-caption;
  color: $c-text-hint;
}
.alert-msg {
  font-size: $fs-body;
  line-height: 1.6;
  display: block;
}
.alert-actions {
  margin-top: $sp-16;
}
.btn-resolve {
  text-align: center;
  padding: $sp-12;
  border-radius: $r-full;
  border: 2rpx solid $c-safe;
  color: $c-safe;
  font-size: $fs-body;
}
</style>
