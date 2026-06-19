<template>
  <view class="page">
    <view class="header">
      <text class="greeting">{{ greeting }}</text>
      <text class="subtitle">今日牵挂状态</text>
    </view>

    <view v-if="userStore.isFamily" class="elder-list">
      <view v-for="elder in elderStatuses" :key="elder.id" class="card elder-card" @tap="goElderStatus(elder)">
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
import { ref, computed } from "vue";
import { onShow } from "@dcloudio/uni-app";
import { useUserStore } from "@/stores/user";
import { useRelationStore } from "@/stores/relation";
import { getElderStatus } from "@/api/elder";
import { formatRelativeTime } from "@/utils/date";

const userStore = useUserStore();
const relationStore = useRelationStore();

const elderStatuses = ref([]);

const greeting = computed(() => {
  const hour = new Date().getHours();
  if (hour < 12) return "早上好";
  if (hour < 18) return "下午好";
  return "晚上好";
});

onShow(async () => {
  if (userStore.isFamily) {
    await relationStore.loadRelations();
    await loadElderStatuses();
  }
});

async function loadElderStatuses() {
  const relations = relationStore.relations;
  const results = await Promise.all(
    relations.map(async (r) => {
      try {
        const status = await getElderStatus(r.elder_user_id);
        return {
          ...r,
          today_read: status.today_read ?? false,
          last_active_text: status.last_active_at
            ? formatRelativeTime(status.last_active_at)
            : "暂无活跃记录",
        };
      } catch {
        return {
          ...r,
          today_read: false,
          last_active_text: "暂无活跃记录",
        };
      }
    })
  );
  elderStatuses.value = results;
}

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
