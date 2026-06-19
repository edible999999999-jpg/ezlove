<template>
  <div v-loading="store.loading">
    <div class="page-header">
      <h2>食堂管理</h2>
    </div>

    <el-card class="section-card">
      <template #header><span>录入就餐数据</span></template>
      <el-form>
        <el-form-item label="文本输入">
          <el-input v-model="rawText" type="textarea" :rows="4" placeholder="例：今天中午食堂，张大爷来了，李奶奶没来" />
        </el-form-item>
        <el-form-item label="或上传 Excel">
          <el-upload ref="uploadRef" :auto-upload="false" :limit="1" accept=".xlsx,.xls" :on-change="handleFileChange">
            <el-button type="primary" plain>选择文件</el-button>
          </el-upload>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="store.submitting" @click="handleSubmit">
            AI 解析并提交
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <template #header><span>历史记录</span></template>
      <el-table :data="store.records" stripe>
        <el-table-column prop="created_at" label="时间" width="180" />
        <el-table-column prop="source_format" label="来源" width="80" />
        <el-table-column prop="parse_status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.parse_status === 'success' ? 'success' : row.parse_status === 'failed' ? 'danger' : 'info'" size="small">
              {{ row.parse_status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="raw_text" label="原始文本" show-overflow-tooltip />
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useCanteenStore } from '@/stores/canteen'
import { ElMessage } from 'element-plus'

const store = useCanteenStore()
const rawText = ref('')
const fileBytes = ref(null)
const uploadRef = ref(null)

onMounted(() => store.load())

function handleFileChange(file) {
  fileBytes.value = file.raw
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
      ElMessage.success('解析成功')
    } else {
      ElMessage.warning('LLM 解析失败，请手动修正')
    }
    rawText.value = ''
    fileBytes.value = null
    if (uploadRef.value) uploadRef.value.clearFiles()
  } catch (e) {
    // handled by interceptor
  }
}
</script>

<style scoped>
.section-card { margin-bottom: 20px; }
</style>
