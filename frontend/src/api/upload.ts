import request from './request'

export interface UploadResult {
  filename: string
  originalName: string
  size: number
}

export const uploadFile = (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  return request.post<unknown, UploadResult>('/api/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}
