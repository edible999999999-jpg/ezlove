<template>
  <div v-loading="store.loading">
    <div class="page-header">
      <div>
        <h2>老人档案</h2>
        <p class="page-desc">管理社区老人信息，设置关爱分级</p>
      </div>
      <el-button type="primary" @click="showDialog = true" :icon="Plus">新增老人</el-button>
    </div>

    <!-- Filters -->
    <div class="filter-bar">
      <el-select v-model="filters.care_level" placeholder="按分级筛选" clearable @change="store.load(filters)" class="filter-select">
        <el-option label="A级（需重点关爱）" value="A" />
        <el-option label="B级（独居需关注）" value="B" />
        <el-option label="C级（健康可互助）" value="C" />
      </el-select>
      <el-input v-model="filters.search" placeholder="搜索姓名..." clearable @input="store.load(filters)" class="filter-search" :prefix-icon="Search" />
    </div>

    <!-- Table -->
    <div class="table-wrapper">
      <el-table :data="store.elders" @row-click="row => $router.push(`/elders/${row.id}`)" :row-class-name="() => 'clickable-row'">
        <el-table-column prop="elder_name" label="姓名" min-width="100">
          <template #default="{ row }">
            <div class="elder-name">
              <div class="name-avatar" :class="`avatar--${row.care_level?.toLowerCase()}`">
                {{ row.elder_name?.charAt(0) }}
              </div>
              <span>{{ row.elder_name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="care_level" label="分级" width="100">
          <template #default="{ row }">
            <span class="care-badge" :class="`care-badge--${row.care_level?.toLowerCase()}`">
              {{ row.care_level }}级
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="address" label="楼栋/门牌" min-width="120" />
        <el-table-column prop="today_active" label="今日状态" width="100">
          <template #default="{ row }">
            <div class="status-cell">
              <span class="status-dot" :class="row.today_active ? 'status-dot--active' : 'status-dot--inactive'"></span>
              {{ row.today_active ? '活跃' : '未活跃' }}
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="health_notes" label="健康备注" min-width="150">
          <template #default="{ row }">
            <span class="text-muted">{{ row.health_notes || '—' }}</span>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- Create Dialog -->
    <el-dialog v-model="showDialog" title="新增老人" width="520px" :close-on-click-modal="false">
      <el-form :model="form" label-width="100px" label-position="top">
        <el-form-item label="老人ID（UUID）">
          <el-input v-model="form.elder_id" placeholder="输入老人的用户ID" />
        </el-form-item>
        <el-form-item label="关爱分级">
          <el-radio-group v-model="form.care_level" class="level-radio">
            <el-radio-button value="A">A级 · 重点关爱</el-radio-button>
            <el-radio-button value="B">B级 · 独居关注</el-radio-button>
            <el-radio-button value="C">C级 · 健康互助</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="楼栋/门牌">
          <el-input v-model="form.address" placeholder="例：1号楼203" />
        </el-form-item>
        <el-form-item label="健康备注">
          <el-input v-model="form.health_notes" type="textarea" :rows="3" placeholder="如：高血压、认知障碍、行动不便等" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="handleCreate">确认添加</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useEldersStore } from '@/stores/elders'
import { ElMessage } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'

const store = useEldersStore()
const showDialog = ref(false)
const filters = reactive({ care_level: '', search: '' })
const form = reactive({ elder_id: '', care_level: 'B', address: '', health_notes: '' })

onMounted(() => store.load())

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
}

.filter-select {
  width: 200px;
}

.filter-search {
  width: 220px;
}

.table-wrapper {
  background: $surface-white;
  border-radius: $radius-md;
  border: 1px solid $warm-paper;
  overflow: hidden;
}

.elder-name {
  display: flex;
  align-items: center;
  gap: $sp-3;
}

.name-avatar {
  width: 32px;
  height: 32px;
  border-radius: $radius-full;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: $fs-sm;
  font-weight: $fw-bold;
  color: #fff;
  flex-shrink: 0;
}

.avatar--a { background: $level-a; }
.avatar--b { background: $level-b; }
.avatar--c { background: $level-c; }

.status-cell {
  display: flex;
  align-items: center;
  gap: $sp-2;
  font-size: $fs-sm;
}

.clickable-row {
  cursor: pointer;
}

.level-radio {
  display: flex;
  gap: $sp-2;
}
</style>
