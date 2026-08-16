<template>
  <el-dialog
    :model-value="visible"
    title="重置密码"
    width="400px"
    @close="handleClose"
  >
    <p style="margin-bottom: 16px; color: #606266;">
      为用户「{{ user?.name || user?.email }}」设置新密码
    </p>
    <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
      <el-form-item label="新密码" prop="password">
        <el-input v-model="form.password" type="password" show-password placeholder="至少6位" />
      </el-form-item>
      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input v-model="form.confirmPassword" type="password" show-password placeholder="再次输入" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确认重置</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { resetUserPassword, type UserItem } from '@/api/users'

const props = defineProps<{
  visible: boolean
  user: UserItem | null
}>()

const emit = defineEmits<{
  'update:visible': [val: boolean]
  success: []
}>()

const formRef = ref<FormInstance>()
const submitLoading = ref(false)
const form = reactive({ password: '', confirmPassword: '' })

const rules: FormRules = {
  password: [{ required: true, min: 6, message: '密码至少6位', trigger: 'blur' }],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (_rule, value, callback) => {
        if (value !== form.password) {
          callback(new Error('两次密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

const handleSubmit = async () => {
  await formRef.value?.validate()
  if (!props.user) return
  submitLoading.value = true
  try {
    await resetUserPassword(props.user.id, form.password)
    ElMessage.success('密码重置成功')
    emit('success')
    handleClose()
  } finally {
    submitLoading.value = false
  }
}

const handleClose = () => {
  formRef.value?.resetFields()
  form.password = ''
  form.confirmPassword = ''
  emit('update:visible', false)
}
</script>
