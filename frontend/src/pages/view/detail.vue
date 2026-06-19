<template>
  <view class="elder-page">
    <view class="moment-card">
      <view class="sender-info">
        <text class="sender-name">{{ moment.sender_nickname || '家人' }}</text>
        <text class="send-time">{{ timeText }}</text>
      </view>

      <view class="content-area">
        <text class="moment-text">{{ moment.text_content }}</text>
        <image
          v-if="moment.media_urls?.length"
          :src="moment.media_urls[0]"
          mode="widthFix"
          class="moment-image"
        />
      </view>
    </view>

    <view class="response-area">
      <text class="response-hint">让Ta知道你看到了</text>
      <view class="emoji-row">
        <view v-for="emoji in emojis" :key="emoji.code" class="emoji-btn" @tap="sendEmoji(emoji.code)">
          <text class="emoji-icon">{{ emoji.icon }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { onLoad } from "@dcloudio/uni-app";
import { getMomentDetail, recordView, sendResponse } from "@/api/moment";
import { formatDateTime } from "@/utils/date";

const moment = ref({});
const momentId = ref("");

const timeText = computed(() => formatDateTime(moment.value.created_at));

const emojis = [
  { code: "thumbsup", icon: "👍" },
  { code: "heart", icon: "❤️" },
  { code: "smile", icon: "😊" },
  { code: "hug", icon: "🤗" },
];

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

async function sendEmoji(code) {
  try {
    await sendResponse(momentId.value, { response_type: "emoji", content: code });
    uni.showToast({ title: "已回应", icon: "success" });
  } catch (e) {
    uni.showToast({ title: "回应失败", icon: "none" });
  }
}
</script>

<style lang="scss" scoped>
.elder-page {
  min-height: 100vh;
  padding: $sp-24;
  background: $c-bg;
}
.moment-card {
  background: $c-surface;
  border-radius: $r-lg;
  padding: $sp-32;
  box-shadow: $shadow-2;
}
.sender-info {
  margin-bottom: $sp-24;
}
.sender-name {
  font-size: $fs-elder-title;
  font-weight: $fw-bold;
  display: block;
}
.send-time {
  font-size: $fs-elder-body;
  color: $c-text-hint;
  margin-top: $sp-8;
}
.moment-text {
  font-size: $fs-elder-body;
  line-height: 1.8;
  display: block;
  margin-bottom: $sp-24;
}
.moment-image {
  width: 100%;
  border-radius: $r-md;
}
.response-area {
  margin-top: $sp-32;
  text-align: center;
}
.response-hint {
  font-size: $fs-elder-body;
  color: $c-text-sub;
  display: block;
  margin-bottom: $sp-24;
}
.emoji-row {
  display: flex;
  justify-content: center;
  gap: $sp-24;
}
.emoji-btn {
  width: 120rpx;
  height: 120rpx;
  background: $c-surface;
  border-radius: $r-lg;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: $shadow-1;
  &:active {
    transform: scale(0.9);
  }
}
.emoji-icon {
  font-size: 64rpx;
}
</style>
