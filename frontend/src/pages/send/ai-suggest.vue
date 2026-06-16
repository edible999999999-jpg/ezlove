<template>
  <view class="page">
    <view class="header-text">
      <text class="title">AI 帮你写牵挂</text>
      <text class="desc">选一条合适的，或者修改后发送</text>
    </view>

    <view v-if="loading" class="loading">
      <u-loading-icon mode="circle" color="#FF8C42" />
      <text class="loading-text">正在为您生成...</text>
    </view>

    <view v-else class="suggestion-list">
      <view
        v-for="(item, index) in suggestions"
        :key="index"
        class="card suggestion-card"
        :class="{ selected: selectedIndex === index }"
        @tap="selectedIndex = index"
      >
        <text class="tag">{{ item.tag }}</text>
        <text class="content">{{ item.text }}</text>
      </view>
    </view>

    <view class="bottom-actions">
      <view class="btn-ai" @tap="regenerate">换一批</view>
      <view class="btn-primary" @tap="useSuggestion">使用这条</view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { getAiSuggestions } from "@/api/ai";

const elderId = ref("");
const suggestions = ref([]);
const selectedIndex = ref(0);
const loading = ref(false);

onLoad((query) => {
  elderId.value = query.elderId;
  loadSuggestions();
});

async function loadSuggestions() {
  loading.value = true;
  try {
    const res = await getAiSuggestions(elderId.value);
    suggestions.value = res.suggestions || [];
    selectedIndex.value = 0;
  } catch (e) {
    uni.showToast({ title: "生成失败，请重试", icon: "none" });
  } finally {
    loading.value = false;
  }
}

function regenerate() {
  loadSuggestions();
}

function useSuggestion() {
  if (suggestions.value.length === 0) return;
  const selected = suggestions.value[selectedIndex.value];
  const pages = getCurrentPages();
  const prevPage = pages[pages.length - 2];
  if (prevPage) {
    prevPage.$vm.textContent = selected.text;
  }
  uni.navigateBack();
}
</script>

<style lang="scss" scoped>
.header-text {
  padding-top: $sp-24;
  margin-bottom: $sp-32;
}
.title {
  font-size: $fs-headline;
  font-weight: $fw-bold;
  display: block;
}
.desc {
  font-size: $fs-body;
  color: $c-text-sub;
  margin-top: $sp-8;
}
.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 200rpx;
}
.loading-text {
  margin-top: $sp-16;
  color: $c-text-hint;
}
.suggestion-card {
  margin-bottom: $sp-16;
  border: 2rpx solid transparent;
  &.selected {
    border-color: $c-primary;
    background: $c-primary-bg;
  }
}
.tag {
  font-size: $fs-body-sm;
  color: $c-primary;
  background: $c-primary-bg;
  padding: $sp-4 $sp-12;
  border-radius: $r-full;
  display: inline-block;
  margin-bottom: $sp-12;
}
.content {
  font-size: $fs-body;
  line-height: 1.6;
  display: block;
}
.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: $sp-16;
  padding: $sp-24;
  background: $c-surface;
  box-shadow: $shadow-3;
}
.btn-ai {
  flex: 1;
  text-align: center;
  padding: $sp-16;
  border-radius: $r-full;
  border: 2rpx solid $c-primary;
  color: $c-primary;
  font-size: $fs-subtitle;
  font-weight: $fw-semibold;
}
.btn-primary {
  flex: 2;
}
</style>
