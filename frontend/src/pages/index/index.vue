<template>
  <view class="page">
    <view class="header">
      <text class="greeting">{{ greeting }}</text>
      <text class="subtitle">今日牵挂状态</text>
    </view>

    <view v-if="userStore.isFamily" class="elder-list">
      <view v-for="elder in relationStore.relations" :key="elder.id" class="card elder-card" @tap="goElderStatus(elder)">
        <view class="elder-info">
          <text class="elder-name">{{ elder.relation_label || '家人' }}</text>
          <view class="status-badge" :class="elder.today_read ? 'read' : 'unread'">
            <text>{{ elder.today_read ? '今日已读' : '今日未读' }}</text>
          </view>
        </view>
        <text class="last-active">{{ elder.last_active_text || '暂无活跃记录' }}</text>
      </view>
    </view>

    <view class="actions">
      <view class="btn-primary send-btn" @tap="goSend">发送牵挂</view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { onShow } from "@dcloudio/uni-app";
import { useUserStore } from "@/stores/user";
import { useRelationStore } from "@/stores/relation";

const userStore = useUserStore();
const relationStore = useRelationStore();

const greeting = computed(() => {
  const hour = new Date().getHours();
  if (hour < 12) return "早上好";
  if (hour < 18) return "下午好";
  return "晚上好";
});

onShow(() => {
  if (userStore.isFamily) {
    relationStore.loadRelations();
  }
});

function goSend() {
  uni.navigateTo({ url: "/pages/send/index" });
}

function goElderStatus(elder) {
  uni.navigateTo({ url: `/pages/elder/status?id=${elder.elder_user_id}` });
}
</script>

<style lang="scss" scoped>
.header {
  padding-top: 120rpx;
  margin-bottom: $sp-32;
}
.greeting {
  font-size: $fs-headline;
  font-weight: $fw-bold;
  display: block;
}
.subtitle {
  font-size: $fs-body;
  color: $c-text-sub;
  margin-top: $sp-8;
}
.elder-card {
  margin-bottom: $sp-16;
}
.elder-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.elder-name {
  font-size: $fs-title;
  font-weight: $fw-semibold;
}
.status-badge {
  padding: $sp-4 $sp-12;
  border-radius: $r-full;
  font-size: $fs-body-sm;
  &.read {
    background: $c-safe-bg;
    color: $c-safe;
  }
  &.unread {
    background: $c-warn-bg;
    color: $c-warn;
  }
}
.last-active {
  font-size: $fs-body-sm;
  color: $c-text-hint;
  margin-top: $sp-8;
}
.actions {
  margin-top: $sp-32;
}
.send-btn {
  width: 100%;
}
</style>
