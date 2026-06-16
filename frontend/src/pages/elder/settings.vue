<template>
  <view class="page">
    <view class="card">
      <text class="section-title">提醒设置</text>
      <view class="setting-row">
        <text>未读提醒时间</text>
        <picker :value="thresholdIndex" :range="thresholdOptions" @change="onThresholdChange">
          <text class="picker-value">{{ thresholdOptions[thresholdIndex] }}</text>
        </picker>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { updateRelation } from "@/api/relation";

const relationId = ref("");
const thresholdIndex = ref(2);
const thresholdOptions = ["6小时", "8小时", "12小时", "24小时"];
const thresholdValues = [6, 8, 12, 24];

onLoad((query) => {
  relationId.value = query.relationId;
  if (query.threshold) {
    const idx = thresholdValues.indexOf(Number(query.threshold));
    if (idx >= 0) thresholdIndex.value = idx;
  }
});

async function onThresholdChange(e) {
  thresholdIndex.value = e.detail.value;
  try {
    await updateRelation(relationId.value, {
      alert_threshold: thresholdValues[thresholdIndex.value],
    });
    uni.showToast({ title: "已保存", icon: "success" });
  } catch (err) {
    uni.showToast({ title: "保存失败", icon: "none" });
  }
}
</script>

<style lang="scss" scoped>
.section-title {
  font-size: $fs-subtitle;
  font-weight: $fw-semibold;
  margin-bottom: $sp-24;
  display: block;
}
.setting-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $sp-16 0;
  border-bottom: 1rpx solid $c-border;
}
.picker-value {
  color: $c-primary;
  font-weight: $fw-medium;
}
</style>
