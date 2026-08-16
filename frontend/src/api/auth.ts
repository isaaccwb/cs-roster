import request from './request'

export interface LoginParams {
  email: string
  password: string
}

export interface UserInfo {
  id: number
  email: string
  name: string
  is_active: number
}

export interface LoginResult {
  token: string
  user: UserInfo
}

export const login = (data: LoginParams) =>
  request.post<any, LoginResult>('/api/auth/login', data)

export const getUserInfo = () =>
  request.get<any, UserInfo>('/api/auth/info')
