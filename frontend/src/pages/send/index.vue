<template>
  <view class="page">
    <view class="photo-section fade-in">
      <view v-if="imageUrl" class="photo-preview" @tap="chooseImage">
        <image :src="imageUrl" mode="aspectFill" class="preview-img" />
        <view class="photo-change">
          <text>点击换一张</text>
        </view>
      </view>
      <view v-else class="photo-placeholder" @tap="chooseImage">
        <text class="photo-icon">📷</text>
        <text class="photo-title">选一张照片</text>
        <text class="photo-hint">分享你身边的事，让家人感受你的生活</text>
      </view>
    </view>

    <view class="text-section fade-in stagger-1">
      <view class="input-wrap">
        <textarea
          v-model="textContent"
          placeholder="随手写两句（可选）"
          :maxlength="100"
          class="input-area"
        />
        <text class="char-count">{{ textContent.length }}/100</text>
      </view>
    </view>

    <view class="elder-section fade-in stagger-2">
      <text class="section-label">分享给</text>
      <view class="elder-picker">
        <view
          v-for="r in relationStore.relations"
          :key="r.id"
          class="elder-chip"
          :class="{ active: selectedElderId === r.elder_user_id }"
          @tap="selectedElderId = r.elder_user_id"
        >
          <view class="chip-avatar">
            <text>{{ (r.relation_label || '家')[0] }}</text>
          </view>
          <text>{{ r.relation_label || '家人' }}</text>
        </view>
      </view>
    </view>

    <view class="bottom-bar">
      <view class="btn-primary generate-btn" :class="{ disabled: !canGenerate }" @tap="handleGenerate">
        <text class="btn-text">生成海报</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRelationStore } from "@/stores/relation";
import { uploadImage } from "@/api/upload";

const relationStore = useRelationStore();

const selectedElderId = ref("");
const textContent = ref("");
const imageUrl = ref("");
const uploadedUrl = ref("");
const uploading = ref(false);

const canGenerate = computed(() => !!uploadedUrl.value && !!selectedElderId.value && !uploading.value);

onMounted(async () => {
  await relationStore.loadRelations();
  if (relationStore.relations.length > 0) {
    selectedElderId.value = relationStore.relations[0].elder_user_id;
  }
});

function chooseImage() {
  uni.chooseImage({
    count: 1,
    sizeType: ["compressed"],
    success: async (res) => {
      imageUrl.value = res.tempFilePaths[0];
      uploading.value = true;
      try {
        uploadedUrl.value = await uploadImage(res.tempFilePaths[0]);
      } catch (e) {
        uni.showToast({ title: "图片上传失败", icon: "none" });
        imageUrl.value = "";
        uploadedUrl.value = "";
      } finally {
        uploading.value = false;
      }
    },
  });
}

function handleGenerate() {
  if (!canGenerate.value) {
    if (!uploadedUrl.value) {
      uni.showToast({ title: "先选一张照片吧", icon: "none" });
    } else if (!selectedElderId.value) {
      uni.showToast({ title: "选择要分享给谁", icon: "none" });
    }
    return;
  }

  uni.setStorageSync("poster_params", {
    image_url: uploadedUrl.value,
    user_text: textContent.value || null,
    elder_id: selectedElderId.value,
  });
  uni.navigateTo({ url: "/pages/send/poster-preview" });
}
</script>

<style lang="scss" scoped>
.photo-section {
  margin-bottom: $sp-20;
}

.photo-placeholder {
  height: 400rpx;
  background: $c-surface;
  border-radius: $r-xl;
  border: 3rpx dashed $c-border;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: $sp-8;
  transition: all $duration-normal $ease-out;
  &:active {
    background: $c-primary-bg;
    border-color: $c-primary-soft;
    transform: scale(0.98);
  }
}

.photo-icon {
  font-size: 80rpx;
}

.photo-title {
  font-size: $fs-title;
  font-weight: $fw-semibold;
  color: $c-text;
}

.photo-hint {
  font-size: $fs-body-sm;
  color: $c-text-hint;
}

.photo-preview {
  position: relative;
  border-radius: $r-xl;
  overflow: hidden;
  box-shadow: $shadow-md;
}

.preview-img {
  width: 100%;
  height: 400rpx;
  display: block;
}

.photo-change {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: $sp-12 0;
  text-align: center;
  background: rgba(45, 32, 22, 0.5);
  color: $c-text-inverse;
  font-size: $fs-body-sm;
}

.text-section {
  background: $c-surface;
  border-radius: $r-xl;
  padding: $sp-24;
  margin-bottom: $sp-20;
  box-shadow: $shadow-sm;
  border: 1rpx solid $c-border-light;
}

.input-wrap {
  position: relative;
}

.input-area {
  width: 100%;
  min-height: 120rpx;
  font-size: $fs-body;
  line-height: $lh-relaxed;
  padding: $sp-12;
  background: $c-bg;
  border-radius: $r-md;
  border: 1rpx solid $c-border-light;
}

.char-count {
  font-size: $fs-caption;
  color: $c-text-hint;
  text-align: right;
  display: block;
  margin-top: $sp-4;
}

.elder-section {
  background: $c-surface;
  border-radius: $r-xl;
  padding: $sp-24;
  margin-bottom: 200rpx;
  box-shadow: $shadow-sm;
  border: 1rpx solid $c-border-light;
}

.section-label {
  font-size: $fs-body;
  font-weight: $fw-semibold;
  color: $c-text;
  margin-bottom: $sp-16;
  display: block;
}

.elder-picker {
  display: flex;
  flex-wrap: wrap;
  gap: $sp-12;
}

.elder-chip {
  display: flex;
  align-items: center;
  gap: $sp-8;
  padding: $sp-8 $sp-20 $sp-8 $sp-8;
  border-radius: $r-full;
  background: $c-bg-warm;
  color: $c-text-sub;
  font-size: $fs-body;
  font-weight: $fw-medium;
  transition: all $duration-normal $ease-out;
  &.active {
    background: $gradient-warm;
    color: $c-text-inverse;
    box-shadow: 0 4rpx 12rpx rgba(196, 116, 92, 0.2);
    .chip-avatar {
      background: rgba(255, 255, 255, 0.3);
    }
  }
}

.chip-avatar {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background: $c-primary-bg;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: $fs-body-sm;
  font-weight: $fw-bold;
  color: $c-primary;
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: $sp-24;
  padding-bottom: calc(#{$sp-24} + env(safe-area-inset-bottom));
  background: $c-surface;
  box-shadow: $shadow-md;
}

.generate-btn {
  width: 100%;
  text-align: center;
  padding: $sp-20 0;
  border-radius: $r-full;
  background: $gradient-warm;
  box-shadow: 0 6rpx 20rpx rgba(196, 116, 92, 0.3);
  transition: all $duration-normal $ease-out;
  &:active {
    transform: scale(0.97);
    box-shadow: 0 2rpx 8rpx rgba(196, 116, 92, 0.2);
  }
  &.disabled {
    opacity: 0.5;
    box-shadow: none;
  }
}

.btn-text {
  font-size: $fs-title;
  font-weight: $fw-bold;
  color: $c-text-inverse;
}
</style>
