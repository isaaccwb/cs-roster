<template>
  <div class="home-container">
    <h1 class="title">欢迎使用 AI Coding 模板</h1>
    <p class="subtitle">告诉 AI 你想要什么功能，即可自动生成前后端代码</p>

    <!-- 数据库连接状态 -->
    <el-card class="status-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>数据库连接状态</span>
          <div>
            <el-button size="small" @click="exportSchema" :loading="exporting" :disabled="dbStatus.status !== 'ok'">导出表结构</el-button>
            <el-button size="small" @click="refresh" :loading="loading">刷新</el-button>
          </div>
        </div>
      </template>

      <div v-if="loading" class="loading-tip">检测中...</div>
      <div v-else>
        <el-descriptions :column="1" border size="small">
          <el-descriptions-item label="连接状态">
            <el-tag :type="dbStatus.status === 'ok' ? 'success' : 'danger'" size="small">
              {{ dbStatus.status === 'ok' ? '已连接' : '连接失败' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="数据库类型">
            {{ dbStatus.type || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="连接地址">
            <code>{{ dbStatus.url || '-' }}</code>
          </el-descriptions-item>
          <el-descriptions-item label="表数量">
            {{ tables.length }} 张表
          </el-descriptions-item>
        </el-descriptions>

        <!-- 表列表 -->
        <div v-if="tables.length" class="table-list">
          <p class="section-title">数据库中的表：</p>
          <el-tag v-for="t in tables" :key="t" size="small" class="table-tag">{{ t }}</el-tag>
        </div>

        <!-- 未连接提示 -->
        <el-alert
          v-if="dbStatus.type === 'SQLite'"
          type="info"
          :closable="false"
          show-icon
          class="tip-alert"
        >
          <template #title>当前使用本地 SQLite（零配置模式）</template>
          <p>如需连接 MySQL，请编辑 <code>backend/.env</code> 文件填入数据库信息后重启后端。</p>
        </el-alert>

        <el-alert
          v-if="dbStatus.type === 'MySQL'"
          type="success"
          :closable="false"
          show-icon
          class="tip-alert"
        >
          <template #title>已连接 MySQL 数据库</template>
          <p>可以告诉 AI："帮我把 {{ tables[0] || 'xxx' }} 表做成一个管理页面"</p>
        </el-alert>

        <el-alert
          v-if="dbStatus.status !== 'ok'"
          type="error"
          :closable="false"
          show-icon
          class="tip-alert"
        >
          <template #title>数据库连接失败</template>
          <p>{{ dbStatus.message || '请检查 backend/.env 中的数据库配置是否正确' }}</p>
        </el-alert>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import request from '@/api/request'

const loading = ref(true)
const exporting = ref(false)
const dbStatus = ref<any>({})
const tables = ref<string[]>([])

async function refresh() {
  loading.value = true
  try {
    const status = await request.get('/api/database/status')
    dbStatus.value = status || {}
  } catch {
    dbStatus.value = { status: 'error', message: '无法连接后端服务' }
  }
  try {
    const t = await request.get('/api/database/tables') as any
    tables.value = (t as string[]) || []
  } catch {
    tables.value = []
  }
  loading.value = false
}

async function exportSchema() {
  exporting.value = true
  try {
    const res = await fetch('/api/database/export-schema')
    if (!res.ok) throw new Error('导出失败')
    const blob = await res.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'schema_export.sql'
    a.click()
    URL.revokeObjectURL(url)
  } catch (e: any) {
    console.error(e)
  } finally {
    exporting.value = false
  }
}

onMounted(refresh)
</script>

<style scoped>
.home-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 40px;
  gap: 16px;
}

.title {
  font-size: 32px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.subtitle {
  font-size: 16px;
  color: var(--el-text-color-secondary);
}

.status-card {
  width: 100%;
  max-width: 600px;
  margin-top: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.loading-tip {
  text-align: center;
  color: var(--el-text-color-secondary);
  padding: 20px;
}

.table-list {
  margin-top: 16px;
}

.section-title {
  font-size: 13px;
  color: var(--el-text-color-secondary);
  margin-bottom: 8px;
}

.table-tag {
  margin: 0 6px 6px 0;
}

.tip-alert {
  margin-top: 16px;
}

code {
  font-family: monospace;
  font-size: 12px;
  background: var(--el-fill-color-light);
  padding: 2px 4px;
  border-radius: 3px;
}
</style>
