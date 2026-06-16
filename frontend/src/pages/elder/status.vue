<template>
  <view class="page">
    <view class="card status-card">
      <text class="elder-name">{{ elderName }}</text>
      <view class="status-indicator" :class="todayRead ? 'online' : 'offline'">
        <text class="status-label">{{ todayRead ? '今日已查看' : '今日未查看' }}</text>
        <text class="last-time">{{ lastActiveText }}</text>
      </view>
    </view>

    <view class="card" style="margin-top: 32rpx;">
      <text class="section-title">最近 7 天</text>
      <view class="calendar-row">
        <view v-for="day in weekDays" :key="day.date" class="day-cell">
          <text class="day-label">{{ day.label }}</text>
          <view class="day-dot" :class="day.active ? 'active' : 'inactive'" />
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { getElderStatus, getElderActivity } from "@/api/elder";

const elderId = ref("");
const elderName = ref("");
const todayRead = ref(false);
const lastActiveText = ref("暂无记录");
const weekDays = ref([]);

onLoad((query) => {
  elderId.value = query.id;
  loadData();
});

async function loadData() {
  try {
    const [status, activity] = await Promise.all([
      getElderStatus(elderId.value),
      getElderActivity(elderId.value, { days: 7 }),
    ]);
    elderName.value = status.elder_name || "家人";
    todayRead.value = status.today_read;
    lastActiveText.value = status.last_active_text || "暂无记录";
    weekDays.value = activity.days || [];
  } catch (e) {
    uni.showToast({ title: "加载失败", icon: "none" });
  }
}
</script>

<style lang="scss" scoped>
.status-card {
  text-align: center;
  padding: $sp-48 $sp-24;
}
.elder-name {
  font-size: $fs-headline;
  font-weight: $fw-bold;
  display: block;
  margin-bottom: $sp-24;
}
.status-indicator {
  padding: $sp-24;
  border-radius: $r-lg;
  &.online { background: $c-safe-bg; }
  &.offline { background: $c-warn-bg; }
}
.status-label {
  font-size: $fs-title;
  font-weight: $fw-semibold;
  display: block;
}
.last-time {
  font-size: $fs-body;
  color: $c-text-sub;
  margin-top: $sp-8;
}
.section-title {
  font-size: $fs-subtitle;
  font-weight: $fw-semibold;
  margin-bottom: $sp-16;
  display: block;
}
.calendar-row {
  display: flex;
  justify-content: space-between;
}
.day-cell {
  text-align: center;
}
.day-label {
  font-size: $fs-body-sm;
  color: $c-text-sub;
  display: block;
  margin-bottom: $sp-8;
}
.day-dot {
  width: 24rpx;
  height: 24rpx;
  border-radius: 50%;
  margin: 0 auto;
  &.active { background: $c-safe; }
  &.inactive { background: $c-border; }
}
</style>
