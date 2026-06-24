<template>
  <view class="page">
    <view v-if="relationStore.relations.length === 0" class="empty-state fade-in">
      <view class="empty-icon-wrap">
        <text class="empty-icon">👨‍👩‍👧</text>
      </view>
      <text class="empty-title">家人还没加入呢</text>
      <text class="empty-desc">把邀请码分享给家人，一起连接彼此的日常</text>
      <view class="btn-primary empty-btn" @tap="goInvite">邀请家人</view>
    </view>

    <view v-else class="relation-list">
      <view
        v-for="(r, index) in relationStore.relations"
        :key="r.id"
        class="relation-card fade-in"
        :class="'stagger-' + Math.min(index + 1, 4)"
      >
        <view class="relation-left">
          <view class="relation-avatar">
            <text class="relation-initial">{{ (r.relation_label || '家')[0] }}</text>
          </view>
          <view class="relation-info">
            <text class="relation-label">{{ r.relation_label || '家人' }}</text>
            <text v-if="r.nickname" class="relation-nickname">{{ r.nickname }}</text>
          </view>
        </view>
        <view class="relation-action" @tap="confirmRemove(r.id)">
          <text class="action-text">解除</text>
        </view>
      </view>
    </view>

    <view v-if="relationStore.relations.length > 0" class="add-area fade-in stagger-3">
      <view class="btn-secondary add-btn" @tap="goInvite">
        <text>+ 添加家人</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { onShow } from "@dcloudio/uni-app";
import { useRelationStore } from "@/stores/relation";

const relationStore = useRelationStore();

onShow(() => {
  relationStore.loadRelations();
});

function goInvite() {
  uni.navigateTo({ url: "/pages/bind/invite" });
}

function confirmRemove(id) {
  uni.showModal({
    title: "确认解除",
    content: "解除后将无法查看对方状态",
    success: async (res) => {
      if (res.confirm) {
        await relationStore.remove(id);
        uni.showToast({ title: "已解除", icon: "success" });
      }
    },
  });
}
</script>

<style lang="scss" scoped>
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

.relation-card {
  background: $c-surface;
  border-radius: $r-lg;
  padding: $sp-24;
  margin-bottom: $sp-12;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: $shadow-sm;
  border: 1rpx solid $c-border-light;
}

.relation-left {
  display: flex;
  align-items: center;
  gap: $sp-16;
}

.relation-avatar {
  width: 80rpx;
  height: 80rpx;
  background: $gradient-warm-soft;
  border-radius: $r-xl;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.relation-initial {
  font-size: $fs-subtitle;
  font-weight: $fw-bold;
  color: $c-primary;
}

.relation-label {
  font-size: $fs-body;
  font-weight: $fw-semibold;
  color: $c-text;
  display: block;
}

.relation-nickname {
  font-size: $fs-body-sm;
  color: $c-text-hint;
  margin-top: $sp-2;
  display: block;
}

.relation-action {
  padding: $sp-8 $sp-16;
  border-radius: $r-full;
  &:active {
    background: $c-warn-bg;
  }
}

.action-text {
  font-size: $fs-body-sm;
  color: $c-warn;
  font-weight: $fw-medium;
}

.add-area {
  margin-top: $sp-24;
}

.add-btn {
  width: 100%;
  text-align: center;
}
</style>
