<template>
  <view class="page">
    <view v-for="r in relationStore.relations" :key="r.id" class="card relation-item">
      <view class="relation-info">
        <text class="label">{{ r.relation_label || '家人' }}</text>
        <text class="nickname">{{ r.nickname || '' }}</text>
      </view>
      <view class="relation-actions">
        <text class="action-text" @tap="confirmRemove(r.id)">解除绑定</text>
      </view>
    </view>

    <view class="add-area">
      <view class="btn-primary" @tap="goInvite">添加家人</view>
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
.relation-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $sp-16;
}
.label {
  font-size: $fs-title;
  font-weight: $fw-semibold;
  display: block;
}
.nickname {
  font-size: $fs-body-sm;
  color: $c-text-hint;
  margin-top: $sp-4;
}
.action-text {
  font-size: $fs-body-sm;
  color: $c-warn;
}
.add-area {
  margin-top: $sp-32;
}
</style>
