<template>
  <div>
    <!-- Page Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h2 class="font-headline text-2xl font-bold text-on-surface">食堂管理</h2>
        <p class="text-on-surface-variant text-sm mt-1">录入就餐数据，AI 自动解析并生成预警</p>
      </div>
    </div>

    <div class="flex flex-col gap-6">
      <!-- Input Card -->
      <div class="bg-white rounded-3xl shadow-sm border border-outline-variant/20 overflow-hidden">
        <div class="px-6 py-5 border-b border-outline-variant/20">
          <h3 class="font-headline text-lg font-bold text-on-surface">录入就餐数据</h3>
        </div>
        <div class="p-6 space-y-5">
          <div>
            <label class="text-sm font-semibold text-charcoal ml-1 block mb-1.5">文本描述</label>
            <textarea
              v-model="rawText"
              rows="4"
              class="w-full px-4 py-3 bg-white border border-outline-variant rounded-xl text-charcoal placeholder:text-outline-variant/60 focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary/30 transition-all resize-none"
              placeholder="例：今天中午食堂，张大爷来了，李奶奶没来，王大爷来了但没怎么吃"
            ></textarea>
          </div>

          <div>
            <label class="text-sm font-semibold text-charcoal ml-1 block mb-1.5">或上传 Excel 文件</label>
            <div
              class="border-2 border-dashed border-outline-variant rounded-2xl p-8 text-center hover:border-primary/40 transition-colors cursor-pointer"
              @click="$refs.fileInput.click()"
              @dragover.prevent
              @drop.prevent="handleFileDrop"
            >
              <span class="material-symbols-outlined text-4xl text-inactive-gray block mb-2">upload_file</span>
              <div class="text-sm text-on-surface-variant">
                <span>将文件拖拽到此处，或</span>
                <span class="text-primary font-semibold ml-1">点击选择</span>
              </div>
              <p v-if="fileBytes" class="text-xs text-secondary font-semibold mt-2">{{ fileBytes.name }}</p>
            </div>
            <input ref="fileInput" type="file" accept=".xlsx,.xls" class="hidden" @change="handleFileChange" />
          </div>

          <button
            :disabled="store.submitting"
            :class="{ 'opacity-80 cursor-not-allowed': store.submitting }"
            class="w-full py-4 bg-primary text-white font-semibold rounded-xl shadow-lg shadow-primary/20 hover:bg-terracotta hover:shadow-xl transition-all duration-200 flex items-center justify-center gap-2"
            @click="handleSubmit"
          >
            <span class="material-symbols-outlined">auto_awesome</span>
            {{ store.submitting ? '解析中...' : 'AI 解析并提交' }}
          </button>
        </div>
      </div>

      <!-- History Card -->
      <div class="bg-white rounded-3xl shadow-sm border border-outline-variant/20 overflow-hidden">
        <div class="px-6 py-5 border-b border-outline-variant/20 flex justify-between items-center">
          <h3 class="font-headline text-lg font-bold text-on-surface">历史记录</h3>
          <button class="flex items-center gap-1 text-sm text-on-surface-variant hover:text-primary transition-colors" @click="store.load()">
            <span class="material-symbols-outlined text-lg">refresh</span>
            刷新
          </button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-outline-variant/20">
                <th class="text-left px-6 py-4 text-xs font-bold text-on-surface-variant tracking-wider uppercase">时间</th>
                <th class="text-left px-6 py-4 text-xs font-bold text-on-surface-variant tracking-wider uppercase">来源</th>
                <th class="text-left px-6 py-4 text-xs font-bold text-on-surface-variant tracking-wider uppercase">状态</th>
                <th class="text-left px-6 py-4 text-xs font-bold text-on-surface-variant tracking-wider uppercase">原始内容</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in store.records" :key="row.id" class="border-b border-outline-variant/10 hover:bg-surface-container/50 transition-colors">
                <td class="px-6 py-4 text-sm text-on-surface-variant whitespace-nowrap">{{ formatTime(row.created_at) }}</td>
                <td class="px-6 py-4">
                  <span
                    :class="[
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold',
                      row.source_format === 'excel' ? 'bg-accent/10 text-accent' : 'bg-surface-container text-on-surface-variant'
                    ]"
                  >
                    {{ row.source_format === 'excel' ? 'Excel' : '文本' }}
                  </span>
                </td>
                <td class="px-6 py-4">
                  <span
                    :class="[
                      'inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold',
                      row.parse_status === 'success' ? 'bg-secondary/10 text-secondary' : row.parse_status === 'failed' ? 'bg-primary/10 text-primary' : 'bg-surface-container text-on-surface-variant'
                    ]"
                  >
                    <span class="w-1.5 h-1.5 rounded-full" :class="row.parse_status === 'success' ? 'bg-secondary' : row.parse_status === 'failed' ? 'bg-primary' : 'bg-inactive-gray'"></span>
                    {{ { success: '已解析', failed: '失败', pending: '解析中' }[row.parse_status] || row.parse_status }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-on-surface max-w-xs truncate">{{ row.raw_text || '—' }}</td>
              </tr>
            </tbody>
          </table>
          <div v-if="!store.records.length && !store.loading" class="text-center py-12">
            <span class="material-symbols-outlined text-4xl text-inactive-gray">restaurant</span>
            <p class="text-inactive-gray text-sm mt-2">暂无就餐记录</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useCanteenStore } from '@/stores/canteen'

const store = useCanteenStore()
const rawText = ref('')
const fileBytes = ref(null)
const fileInput = ref(null)

onMounted(() => store.load())

function handleFileChange(e) {
  const file = e.target.files?.[0]
  if (file) fileBytes.value = file
}

function handleFileDrop(e) {
  const file = e.dataTransfer?.files?.[0]
  if (file && (file.name.endsWith('.xlsx') || file.name.endsWith('.xls'))) {
    fileBytes.value = file
  }
}

function formatTime(t) {
  if (!t) return '—'
  return new Date(t).toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

async function handleSubmit() {
  if (!rawText.value && !fileBytes.value) {
    return
  }
  const formData = new FormData()
  if (rawText.value) formData.append('raw_text', rawText.value)
  if (fileBytes.value) formData.append('file', fileBytes.value)

  try {
    await store.submit(formData)
    rawText.value = ''
    fileBytes.value = null
    if (fileInput.value) fileInput.value.value = ''
  } catch (e) {
    // handled by interceptor
  }
}
</script>
