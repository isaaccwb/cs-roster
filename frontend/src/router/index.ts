import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { getToken } from '@/utils/auth'
const routes: RouteRecordRaw[] = [
  { path: '/login', name: 'Login', component: () => import('@/views/Login/index.vue'), meta: { title: 'Login', public: true } },
  { path: '/', component: () => import('@/views/Layout/index.vue'), redirect: '/scheduler', children: [
    { path: '/scheduler', name: 'Scheduler', component: () => import('@/views/Scheduler/index.vue'), meta: { title: 'Shift Scheduler' } },
    { path: '/users', name: 'Users', component: () => import('@/views/Users/index.vue'), meta: { title: 'User Management' } },
    { path: '/home', name: 'Home', component: () => import('@/views/Home/index.vue'), meta: { title: 'Home' } }
  ]}
]
const router = createRouter({ history: createWebHistory(), routes })
router.beforeEach((to, _from, next) => {
  if (to.meta.public) { next(); return }
  if (!getToken()) { next({ path: '/login', query: { redirect: to.fullPath } }); return }
  next()
})
export default router
