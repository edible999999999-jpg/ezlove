<template>
  <div v-loading="store.loading">
    <div class="page-header">
      <div>
        <h2>事件中心</h2>
        <p class="page-desc">查看和处理社区老人相关事件</p>
      </div>
      <el-button type="primary" @click="showDialog = true" :icon="Plus">手动新增</el-button>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <el-select v-model="filters.severity" placeholder="严重程度" clearable @change="store.load(filters)">
        <el-option label="紧急" value="urgent" />
        <el-option label="警告" value="warning" />
        <el-option label="信息" value="info" />
      </el-select>
      <el-select v-model="filters.event_type" placeholder="事件类型" clearable @change="store.load(filters)">
        <el-option label="跌倒" value="fall" />
        <el-option label="缺勤" value="absent" />
        <el-option label="紧急" value="emergency" />
        <el-option label="探访" value="visit" />
        <el-option label="其他" value="other" />
      </el-select>
      <el-select v-model="filters.is_resolved" placeholder="处理状态" clearable @change="store.load(filters)">
        <el-option label="未处理" :value="false" />
        <el-option label="已处理" :value="true" />
      </el-select>
    </div>

    <!-- Events Table -->
    <div class="table-wrapper">
      <el-table :data="store.events">
        <el-table-column prop="severity" label="级别" width="90">
          <template #default="{ row }">
            <div class="severity-badge" :class="`severity--${row.severity}`">
              <span class="severity-dot"></span>
              {{ severityLabel(row.severity) }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="event_type" label="类型" width="80">
          <template #default="{ row }">
            <span class="type-label">{{ typeLabel(row.event_type) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200">
          <template #default="{ row }">
            <span class="desc-text">{{ row.description || '—' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="source" label="来源" width="80">
          <template #default="{ row }">
            <el-tag size="small" type="info" disable-transitions>{{ sourceLabel(row.source) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="is_resolved" label="状态" width="90">
          <template #default="{ row }">
            <div class="resolve-status" :class="row.is_resolved ? 'resolved' : 'unresolved'">
              <span class="resolve-dot"></span>
              {{ row.is_resolved ? '已处理' : '待处理' }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="时间" width="160">
          <template #default="{ row }">
            <span class="text-muted">{{ formatTime(row.created_at) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="90" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="!row.is_resolved"
              size="small"
              type="primary"
              @click.stop="handleResolve(row.id)"
            >
              处理
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- Create Dialog -->
    <el-dialog v-model="showDialog" title="新增事件" width="520px" :close-on-click-modal="false">
      <el-form :model="form" label-position="top">
        <el-form-item label="老人ID">
          <el-input v-model="form.elder_id" placeholder="UUID" />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="事件类型">
              <el-select v-model="form.event_type" style="width: 100%">
                <el-option label="跌倒" value="fall" />
                <el-option label="缺勤" value="absent" />
                <el-option label="紧急" value="emergency" />
                <el-option label="探访" value="visit" />
                <el-option label="其他" value="other" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="严重程度">
              <el-select v-model="form.severity" style="width: 100%">
                <el-option label="信息" value="info" />
                <el-option label="警告" value="warning" />
                <el-option label="紧急" value="urgent" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="描述事件详情..." />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">确认创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useEventsStore } from '@/stores/events'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'

const store = useEventsStore()
const showDialog = ref(false)
const filters = reactive({ severity: '', event_type: '', is_resolved: null })
const form = reactive({ elder_id: '', event_type: 'other', severity: 'info', description: '' })

onMounted(() => store.load())

function severityLabel(s) {
  return { urgent: '紧急', warning: '警告', info: '信息' }[s] || s
}
function typeLabel(t) {
  return { fall: '跌倒', absent: '缺勤', emergency: '紧急', visit: '探访', other: '其他' }[t] || t
}
function sourceLabel(s) {
  return { canteen: '食堂', alert: '预警', manual: '手动' }[s] || s
}
function formatTime(t) {
  if (!t) return '—'
  return new Date(t).toLocaleString('zh-CN', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
}

async function handleResolve(id) {
  try {
    await store.resolve(id)
    ElMessage.success('已标记为处理完成')
  } catch (e) {
    // handled by interceptor
  }
}

async function handleCreate() {
  if (!form.elder_id) {
    ElMessage.warning('请填写老人ID')
    return
  }
  try {
    await store.create(form)
    showDialog.value = false
    ElMessage.success('事件已创建')
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

.filter-bar {
  display: flex;
  gap: $sp-3;
  margin-bottom: $sp-5;

  .el-select {
    width: 160px;
  }
}

.table-wrapper {
  background: $surface-white;
  border-radius: $radius-md;
  border: 1px solid $warm-paper;
  overflow: hidden;
}

.severity-badge {
  display: inline-flex;
  align-items: center;
  gap: $sp-1;
  font-size: $fs-sm;
  font-weight: $fw-semibold;
}

.severity-dot {
  width: 8px;
  height: 8px;
  border-radius: $radius-full;
}

.severity--urgent {
  color: $severity-urgent;
  .severity-dot { background: $severity-urgent; box-shadow: 0 0 0 3px rgba(196, 77, 62, 0.15); }
}
.severity--warning {
  color: $severity-warning;
  .severity-dot { background: $severity-warning; box-shadow: 0 0 0 3px rgba(196, 148, 62, 0.15); }
}
.severity--info {
  color: $severity-info;
  .severity-dot { background: $severity-info; box-shadow: 0 0 0 3px rgba(143, 136, 128, 0.1); }
}

.type-label {
  font-size: $fs-sm;
  color: $text-regular;
}

.desc-text {
  font-size: $fs-sm;
  color: $text-primary;
}

.resolve-status {
  display: inline-flex;
  align-items: center;
  gap: $sp-1;
  font-size: $fs-sm;
  font-weight: $fw-medium;
}

.resolve-dot {
  width: 6px;
  height: 6px;
  border-radius: $radius-full;
}

.resolved {
  color: $status-active;
  .resolve-dot { background: $status-active; }
}

.unresolved {
  color: $level-a;
  .resolve-dot { background: $level-a; }
}
</style>
