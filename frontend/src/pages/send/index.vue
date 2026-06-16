<template>
  <view class="page">
    <view class="card">
      <text class="section-title">选择家人</text>
      <view class="elder-picker">
        <view
          v-for="r in relationStore.relations"
          :key="r.id"
          class="elder-chip"
          :class="{ active: selectedElderId === r.elder_user_id }"
          @tap="selectedElderId = r.elder_user_id"
        >
          <text>{{ r.relation_label || '家人' }}</text>
        </view>
      </view>
    </view>

    <view class="card" style="margin-top: 32rpx;">
      <text class="section-title">写点什么</text>
      <textarea
        v-model="textContent"
        placeholder="今天想和Ta说点什么..."
        :maxlength="200"
        class="input-area"
      />
      <text class="char-count">{{ textContent.length }}/200</text>
    </view>

    <view class="card" style="margin-top: 32rpx;">
      <text class="section-title">配张图</text>
      <view class="image-area">
        <image v-if="imageUrl" :src="imageUrl" mode="aspectFill" class="preview-img" @tap="chooseImage" />
        <view v-else class="add-image" @tap="chooseImage">
          <text class="add-icon">+</text>
          <text class="add-text">选择图片</text>
        </view>
      </view>
    </view>

    <view class="bottom-actions">
      <view class="btn-ai" @tap="goAiSuggest">AI 帮我写</view>
      <view class="btn-primary" @tap="handleSend">发送牵挂</view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRelationStore } from "@/stores/relation";
import { useMomentStore } from "@/stores/moment";

const relationStore = useRelationStore();
const momentStore = useMomentStore();

const selectedElderId = ref("");
const textContent = ref("");
const imageUrl = ref("");

onMounted(() => {
  relationStore.loadRelations();
  if (relationStore.relations.length > 0) {
    selectedElderId.value = relationStore.relations[0].elder_user_id;
  }
});

function chooseImage() {
  uni.chooseImage({
    count: 1,
    sizeType: ["compressed"],
    success: (res) => {
      imageUrl.value = res.tempFilePaths[0];
    },
  });
}

async function handleSend() {
  if (!selectedElderId.value) {
    uni.showToast({ title: "请先选择家人", icon: "none" });
    return;
  }
  if (!textContent.value && !imageUrl.value) {
    uni.showToast({ title: "写点什么或配张图吧", icon: "none" });
    return;
  }
  try {
    uni.showLoading({ title: "发送中..." });
    await momentStore.send({
      elder_id: selectedElderId.value,
      text_content: textContent.value,
      media_urls: imageUrl.value ? [imageUrl.value] : [],
    });
    uni.hideLoading();
    uni.showToast({ title: "已发送", icon: "success" });
    setTimeout(() => uni.navigateBack(), 1500);
  } catch (e) {
    uni.hideLoading();
    uni.showToast({ title: e.message, icon: "none" });
  }
}

function goAiSuggest() {
  uni.navigateTo({ url: `/pages/send/ai-suggest?elderId=${selectedElderId.value}` });
}
</script>

<style lang="scss" scoped>
.section-title {
  font-size: $fs-subtitle;
  font-weight: $fw-semibold;
  margin-bottom: $sp-16;
  display: block;
}
.elder-picker {
  display: flex;
  flex-wrap: wrap;
  gap: $sp-12;
}
.elder-chip {
  padding: $sp-8 $sp-20;
  border-radius: $r-full;
  background: $c-primary-bg;
  color: $c-text-sub;
  font-size: $fs-body;
  &.active {
    background: $c-primary;
    color: #FFFFFF;
  }
}
.input-area {
  width: 100%;
  min-height: 200rpx;
  font-size: $fs-body;
  line-height: 1.6;
  padding: $sp-12;
  background: $c-bg;
  border-radius: $r-md;
}
.char-count {
  font-size: $fs-caption;
  color: $c-text-hint;
  text-align: right;
  display: block;
  margin-top: $sp-4;
}
.image-area {
  display: flex;
}
.preview-img {
  width: 200rpx;
  height: 200rpx;
  border-radius: $r-md;
}
.add-image {
  width: 200rpx;
  height: 200rpx;
  border: 2rpx dashed $c-border;
  border-radius: $r-md;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.add-icon {
  font-size: $fs-headline;
  color: $c-text-hint;
}
.add-text {
  font-size: $fs-body-sm;
  color: $c-text-hint;
  margin-top: $sp-4;
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
