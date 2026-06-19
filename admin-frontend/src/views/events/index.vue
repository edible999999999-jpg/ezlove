<template>
  <div v-loading="store.loading">
    <div class="page-header">
      <h2>事件中心</h2>
      <el-button type="primary" @click="showDialog = true">手动新增</el-button>
    </div>

    <el-row :gutter="16" style="margin-bottom: 16px">
      <el-col :span="6">
        <el-select v-model="filters.severity" placeholder="严重程度" clearable @change="store.load(filters)">
          <el-option label="紧急" value="urgent" />
          <el-option label="警告" value="warning" />
          <el-option label="信息" value="info" />
        </el-select>
      </el-col>
      <el-col :span="6">
        <el-select v-model="filters.event_type" placeholder="事件类型" clearable @change="store.load(filters)">
          <el-option label="跌倒" value="fall" />
          <el-option label="缺勤" value="absent" />
          <el-option label="紧急" value="emergency" />
          <el-option label="探访" value="visit" />
          <el-option label="其他" value="other" />
        </el-select>
      </el-col>
      <el-col :span="6">
        <el-select v-model="filters.is_resolved" placeholder="处理状态" clearable @change="store.load(filters)">
          <el-option label="未处理" :value="false" />
          <el-option label="已处理" :value="true" />
        </el-select>
      </el-col>
    </el-row>

    <el-table :data="store.events" stripe>
      <el-table-column prop="severity" label="级别" width="80">
        <template #default="{ row }">
          <el-tag :type="severityType(row.severity)" size="small">{{ severityLabel(row.severity) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="event_type" label="类型" width="80" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="is_resolved" label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_resolved ? 'success' : 'danger'" size="small">
            {{ row.is_resolved ? '已处理' : '未处理' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="时间" width="180" />
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button v-if="!row.is_resolved" size="small" type="primary" @click="handleResolve(row.id)">
            处理
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showDialog" title="新增事件" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="老人ID">
          <el-input v-model="form.elder_id" placeholder="UUID" />
        </el-form-item>
        <el-form-item label="事件类型">
          <el-select v-model="form.event_type">
            <el-option label="跌倒" value="fall" />
            <el-option label="缺勤" value="absent" />
            <el-option label="紧急" value="emergency" />
            <el-option label="探访" value="visit" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="严重程度">
          <el-select v-model="form.severity">
            <el-option label="信息" value="info" />
            <el-option label="警告" value="warning" />
            <el-option label="紧急" value="urgent" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useEventsStore } from '@/stores/events'
import { ElMessage } from 'element-plus'

const store = useEventsStore()
const showDialog = ref(false)
const filters = reactive({ severity: '', event_type: '', is_resolved: null })
const form = reactive({ elder_id: '', event_type: 'other', severity: 'info', description: '' })

onMounted(() => store.load())

function severityType(s) {
  return { urgent: 'danger', warning: 'warning', info: 'info' }[s] || 'info'
}
function severityLabel(s) {
  return { urgent: '紧急', warning: '警告', info: '信息' }[s] || s
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
