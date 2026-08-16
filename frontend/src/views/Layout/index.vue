<template>
  <el-container class="layout-container">
    <el-aside width="220px">
      <div class="logo">CS Roster</div>
      <el-menu :default-active="route.path" router background-color="#304156" text-color="#bfcbd9" active-text-color="#409eff">
        <el-menu-item index="/scheduler"><el-icon><Calendar /></el-icon><span>Shift Scheduler</span></el-menu-item>
        <el-menu-item index="/users"><el-icon><User /></el-icon><span>User Management</span></el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="layout-header">
        <span class="page-title">{{ route.meta.title }}</span>
        <div class="header-right">
          <span class="user-name">{{ userName }}</span>
          <el-button type="danger" text @click="handleLogout">Logout</el-button>
        </div>
      </el-header>
      <el-main><router-view /></el-main>
    </el-container>
  </el-container>
</template>
<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { User, Calendar } from '@element-plus/icons-vue'
import { getUserInfo } from '@/api/auth'
import { removeToken } from '@/utils/auth'
const route = useRoute()
const router = useRouter()
const userName = ref('')
onMounted(async () => { try { const u = await getUserInfo(); userName.value = u.name || u.email } catch {} })
const handleLogout = () => { removeToken(); router.push('/login') }
</script>
<style scoped>
.layout-container{height:100vh}.logo{height:60px;line-height:60px;text-align:center;font-size:18px;font-weight:bold;color:#fff;background:#263445}.el-aside{background:#304156}.layout-header{display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #e6e6e6;background:#fff}.page-title{font-size:16px;font-weight:500}.header-right{display:flex;align-items:center;gap:12px}.user-name{font-size:14px;color:#606266}
</style>
