<template>
  <div v-loading="store.loading">
    <div class="page-header">
      <div>
        <h2>食堂管理</h2>
        <p class="page-desc">录入就餐数据，AI 自动解析并生成预警</p>
      </div>
    </div>

    <div class="canteen-grid">
      <!-- Input Card -->
      <div class="input-card animate-fade-in-up">
        <div class="card-header">
          <h3 class="card-title">录入就餐数据</h3>
        </div>

        <div class="card-body">
          <el-form label-position="top">
            <el-form-item label="文本描述">
              <el-input
                v-model="rawText"
                type="textarea"
                :rows="4"
                placeholder="例：今天中午食堂，张大爷来了，李奶奶没来，王大爷来了但没怎么吃"
              />
            </el-form-item>

            <el-form-item label="或上传 Excel 文件">
              <el-upload
                ref="uploadRef"
                :auto-upload="false"
                :limit="1"
                accept=".xlsx,.xls"
                :on-change="handleFileChange"
                :on-remove="handleFileRemove"
                class="upload-area"
                drag
              >
                <el-icon :size="24" color="#C4BAB0"><UploadFilled /></el-icon>
                <div class="upload-text">
                  <span>将文件拖拽到此处，或</span>
                  <el-button type="primary" text>点击选择</el-button>
                </div>
              </el-upload>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                :loading="store.submitting"
                @click="handleSubmit"
                size="large"
                class="submit-btn"
              >
                <el-icon><MagicStick /></el-icon>
                AI 解析并提交
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <!-- History Card -->
      <div class="history-card animate-fade-in-up" style="animation-delay: 120ms">
        <div class="card-header">
          <h3 class="card-title">历史记录</h3>
          <el-button text @click="store.load()" :icon="Refresh">刷新</el-button>
        </div>

        <div class="card-body">
          <el-table :data="store.records" size="small">
            <el-table-column prop="created_at" label="时间" width="160">
              <template #default="{ row }">
                <span class="text-muted">{{ formatTime(row.created_at) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="source_format" label="来源" width="80">
              <template #default="{ row }">
                <el-tag size="small" :type="row.source_format === 'excel' ? 'warning' : 'info'" disable-transitions>
                  {{ row.source_format === 'excel' ? 'Excel' : '文本' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="parse_status" label="状态" width="90">
              <template #default="{ row }">
                <el-tag
                  size="small"
                  :type="row.parse_status === 'success' ? 'success' : row.parse_status === 'failed' ? 'danger' : 'info'"
                  disable-transitions
                >
                  {{ { success: '已解析', failed: '失败', pending: '解析中' }[row.parse_status] || row.parse_status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="raw_text" label="原始内容" show-overflow-tooltip />
          </el-table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useCanteenStore } from '@/stores/canteen'
import { ElMessage } from 'element-plus'
import { UploadFilled, MagicStick, Refresh } from '@element-plus/icons-vue'

const store = useCanteenStore()
const rawText = ref('')
const fileBytes = ref(null)
const uploadRef = ref(null)

onMounted(() => store.load())

function handleFileChange(file) {
  fileBytes.value = file.raw
}

function handleFileRemove() {
  fileBytes.value = null
}

function formatTime(t) {
  if (!t) return '—'
  return new Date(t).toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

async function handleSubmit() {
  if (!rawText.value && !fileBytes.value) {
    ElMessage.warning('请输入文本或上传文件')
    return
  }
  const formData = new FormData()
  if (rawText.value) formData.append('raw_text', rawText.value)
  if (fileBytes.value) formData.append('file', fileBytes.value)

  try {
    const result = await store.submit(formData)
    if (result.parse_status === 'success') {
      ElMessage.success('解析成功，已生成就餐记录')
    } else {
      ElMessage.warning('LLM 解析失败，请检查输入或手动修正')
    }
    rawText.value = ''
    fileBytes.value = null
    if (uploadRef.value) uploadRef.value.clearFiles()
  } catch (e) {
    // handled by interceptor
  }
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.page-desc {
  font-size: $fs-sm;
  color: $text-secondary;
  margin-top: $sp-1;
}

.canteen-grid {
  display: flex;
  flex-direction: column;
  gap: $sp-5;
}

.input-card,
.history-card {
  background: $surface-white;
  border: 1px solid $warm-paper;
  border-radius: $radius-md;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: $sp-4 $sp-5;
  border-bottom: 1px solid $warm-paper;
}

.card-title {
  font-family: $font-display;
  font-size: $fs-md;
  font-weight: $fw-semibold;
  color: $text-primary;
}

.card-body {
  padding: $sp-5;
}

.upload-area {
  width: 100%;

  :deep(.el-upload-dragger) {
    border: 2px dashed $warm-sand;
    border-radius: $radius-md;
    padding: $sp-6;
    transition: border-color $duration-normal $ease-out;

    &:hover {
      border-color: $brand-terracotta-light;
    }
  }
}

.upload-text {
  margin-top: $sp-2;
  font-size: $fs-sm;
  color: $text-secondary;
  display: flex;
  align-items: center;
  gap: $sp-1;
}

.submit-btn {
  width: 100%;
  height: 48px;
  font-size: $fs-md;
  font-weight: $fw-semibold;
}
</style>
