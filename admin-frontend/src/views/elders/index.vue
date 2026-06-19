<template>
  <div v-loading="store.loading">
    <div class="page-header">
      <h2>老人档案</h2>
      <el-button type="primary" @click="showDialog = true">新增老人</el-button>
    </div>

    <el-row :gutter="16" style="margin-bottom: 16px">
      <el-col :span="6">
        <el-select v-model="filters.care_level" placeholder="按分级筛选" clearable @change="store.load(filters)">
          <el-option label="A级" value="A" />
          <el-option label="B级" value="B" />
          <el-option label="C级" value="C" />
        </el-select>
      </el-col>
      <el-col :span="6">
        <el-input v-model="filters.search" placeholder="搜索姓名" clearable @input="store.load(filters)" />
      </el-col>
    </el-row>

    <el-table :data="store.elders" stripe @row-click="row => $router.push(`/elders/${row.id}`)">
      <el-table-column prop="elder_name" label="姓名" />
      <el-table-column prop="care_level" label="分级" width="80">
        <template #default="{ row }">
          <el-tag :type="levelTagType(row.care_level)">{{ row.care_level }}级</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="address" label="楼栋/门牌" />
      <el-table-column prop="today_active" label="今日状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.today_active ? 'success' : 'danger'" size="small">
            {{ row.today_active ? '活跃' : '未活跃' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="health_notes" label="健康备注" />
    </el-table>

    <el-dialog v-model="showDialog" title="新增老人" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="老人ID">
          <el-input v-model="form.elder_id" placeholder="UUID" />
        </el-form-item>
        <el-form-item label="分级">
          <el-radio-group v-model="form.care_level">
            <el-radio value="A">A级</el-radio>
            <el-radio value="B">B级</el-radio>
            <el-radio value="C">C级</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="地址">
          <el-input v-model="form.address" placeholder="楼栋/门牌号" />
        </el-form-item>
        <el-form-item label="健康备注">
          <el-input v-model="form.health_notes" type="textarea" />
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
import { useEldersStore } from '@/stores/elders'
import { ElMessage } from 'element-plus'

const store = useEldersStore()
const showDialog = ref(false)
const filters = reactive({ care_level: '', search: '' })
const form = reactive({ elder_id: '', care_level: 'B', address: '', health_notes: '' })

onMounted(() => store.load())

function levelTagType(level) {
  return { A: 'danger', B: 'warning', C: 'success' }[level] || 'info'
}

async function handleCreate() {
  if (!form.elder_id || !form.care_level) {
    ElMessage.warning('请填写必填项')
    return
  }
  try {
    await store.create(form)
    showDialog.value = false
    ElMessage.success('添加成功')
  } catch (e) {
    // handled by interceptor
  }
}
</script>
