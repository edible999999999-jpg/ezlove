<template>
  <view class="elder-page">
    <view class="moment-card fade-in">
      <view class="sender-row">
        <view class="sender-avatar">
          <text class="sender-initial">{{ (moment.sender_name || '家')[0] }}</text>
        </view>
        <view class="sender-meta">
          <text class="sender-name">{{ moment.sender_name || '家人' }}</text>
          <text class="send-time">{{ moment.time_text || '' }}</text>
        </view>
      </view>

      <view class="divider" />

      <view class="content-area">
        <view v-if="moment.content_type === 'poster' && moment.media_urls?.length" class="poster-area">
          <image
            :src="getFullUrl(moment.media_urls[0])"
            mode="widthFix"
            class="poster-image"
            @tap="previewPoster"
          />
        </view>
        <view v-else>
          <text class="moment-text">{{ moment.text_content }}</text>
          <image
            v-if="moment.media_urls?.length"
            :src="getFullUrl(moment.media_urls[0])"
            mode="widthFix"
            class="moment-image"
          />
        </view>
      </view>
    </view>

    <view class="read-hint fade-in stagger-2">
      <text class="hint-text">已收到，家人会知道你看过了</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { getMomentDetail, recordView } from "@/api/moment";

const BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://localhost:8001"
    : "https://yuxilab.cn/ezlove";

const moment = ref({});
const momentId = ref("");

function getFullUrl(url) {
  if (!url) return "";
  if (url.startsWith("http")) return url;
  return `${BASE_URL}${url}`;
}

onLoad((query) => {
  momentId.value = query.id;
  loadMoment();
});

async function loadMoment() {
  try {
    moment.value = await getMomentDetail(momentId.value);
    await recordView(momentId.value);
  } catch (e) {
    uni.showToast({ title: "内容加载失败", icon: "none" });
  }
}

function previewPoster() {
  if (moment.value.media_urls?.length) {
    uni.previewImage({
      urls: [getFullUrl(moment.value.media_urls[0])],
    });
  }
}
</script>

<style lang="scss" scoped>
.elder-page {
  min-height: 100vh;
  padding: $sp-32;
  padding-bottom: 200rpx;
  background: $gradient-page;
}

.moment-card {
  background: $c-surface;
  border-radius: $r-xl;
  padding: $sp-48 $sp-40;
  box-shadow: $shadow-md;
}

.sender-row {
  display: flex;
  align-items: center;
}

.sender-avatar {
  width: 140rpx;
  height: 140rpx;
  background: $gradient-warm-soft;
  border-radius: $r-xl;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: $sp-24;
  flex-shrink: 0;
}

.sender-initial {
  font-size: $fs-elder-headline;
  font-weight: $fw-bold;
  color: $c-primary;
}

.sender-meta {
  flex: 1;
}

.sender-name {
  font-size: $fs-elder-headline;
  font-weight: $fw-bold;
  color: $c-text;
  display: block;
}

.send-time {
  font-size: $fs-elder-body;
  color: $c-text-hint;
  margin-top: $sp-8;
  display: block;
}

.divider {
  height: 2rpx;
  background: $c-border-light;
  margin: $sp-40 0;
}

.moment-text {
  font-size: $fs-elder-title;
  line-height: $lh-relaxed;
  color: $c-text;
  display: block;
  margin-bottom: $sp-32;
}

.moment-image {
  width: 100%;
  border-radius: $r-lg;
  margin-top: $sp-24;
}

.poster-area {
  margin: 0 (-$sp-40);
}

.poster-image {
  width: 100%;
  display: block;
}

.read-hint {
  margin-top: $sp-48;
  text-align: center;
}

.hint-text {
  font-size: $fs-elder-body;
  color: $c-text-hint;
}
</style>
