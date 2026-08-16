import request from './request'

export interface SchedulerStateResponse {
  id: number
  key: string
  data: Record<string, unknown>
  updatedBy: string
  updatedAt: string
}

export const getSchedulerState = () =>
  request.get<unknown, SchedulerStateResponse | null>('/api/scheduler/state')

export const saveSchedulerState = (data: Record<string, unknown>) =>
  request.put<unknown, SchedulerStateResponse>('/api/scheduler/state', { data })
