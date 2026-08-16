import request from './request'

export interface UserItem {
  id: number
  email: string
  name: string
  is_active: number
  can_edit_scheduler: number
}

export interface UserListParams {
  page?: number
  page_size?: number
  keyword?: string
}

export interface CreateUserData {
  email: string
  name: string
  password: string
}

export interface UpdateUserData {
  email?: string
  name?: string
  is_active?: number
  can_edit_scheduler?: number
}

export const getUserList = (params: UserListParams) =>
  request.get<unknown, { list: UserItem[]; total: number }>('/api/users/list', { params })

export const createUser = (data: CreateUserData) =>
  request.post<unknown, UserItem>('/api/users/create', data)

export const updateUser = (id: number, data: UpdateUserData) =>
  request.put<unknown, UserItem>(`/api/users/update/${id}`, data)

export const resetUserPassword = (id: number, password: string) =>
  request.post<unknown, null>(`/api/users/reset-password/${id}`, { password })

export const deleteUser = (id: number) =>
  request.delete<unknown, null>(`/api/users/delete/${id}`)
