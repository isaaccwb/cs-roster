<template>
  <el-dialog
    :model-value="visible"
    :title="editData ? '编辑用户' : '新增用户'"
    width="460px"
    @close="handleClose"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="form.email" placeholder="user@example.com" />
      </el-form-item>
      <el-form-item label="姓名" prop="name">
        <el-input v-model="form.name" placeholder="显示名称" />
      </el-form-item>
      <el-form-item v-if="!editData" label="密码" prop="password">
        <el-input v-model="form.password" type="password" show-password placeholder="至少6位" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" :loading="submitLoading" @click="handleSubmit">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { createUser, updateUser, type UserItem } from '@/api/users'

const props = defineProps<{
  visible: boolean
  editData: UserItem | null
}>()

const emit = defineEmits<{
  'update:visible': [val: boolean]
  success: []
}>()

const formRef = ref<FormInstance>()
const submitLoading = ref(false)
const form = ref({ email: '', name: '', password: '' })

const rules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' },
  ],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  password: [{ required: true, min: 6, message: '密码至少6位', trigger: 'blur' }],
}

watch(() => props.visible, (val) => {
  if (val && props.editData) {
    form.value = { email: props.editData.email, name: props.editData.name, password: '' }
  } else if (val) {
    form.value = { email: '', name: '', password: '' }
  }
})

const handleSubmit = async () => {
  await formRef.value?.validate()
  submitLoading.value = true
  try {
    if (props.editData) {
      await updateUser(props.editData.id, { email: form.value.email, name: form.value.name })
    } else {
      await createUser(form.value)
    }
    ElMessage.success(props.editData ? '更新成功' : '创建成功')
    emit('success')
    handleClose()
  } finally {
    submitLoading.value = false
  }
}

const handleClose = () => {
  formRef.value?.resetFields()
  emit('update:visible', false)
}
</script>
