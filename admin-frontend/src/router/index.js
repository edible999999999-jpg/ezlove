import { createRouter, createWebHistory } from 'vue-router'
import axios from 'axios'

const routes = [
  { path: '/login', name: 'Login', component: () => import('@/views/login/index.vue') },
  {
    path: '/',
    component: () => import('@/views/layout/index.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/index.vue') },
      { path: 'elders', name: 'Elders', component: () => import('@/views/elders/index.vue') },
      { path: 'elders/:id', name: 'ElderDetail', component: () => import('@/views/elders/detail.vue') },
      { path: 'canteen', name: 'Canteen', component: () => import('@/views/canteen/index.vue') },
      { path: 'events', name: 'Events', component: () => import('@/views/events/index.vue') },
      { path: 'agent', name: 'Agent', component: () => import('@/views/agent/index.vue') },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

function isTokenExpired(token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]))
    return payload.exp * 1000 < Date.now()
  } catch {
    return true
  }
}

function clearAuthAndRedirect(next) {
  localStorage.removeItem('community_access_token')
  localStorage.removeItem('community_refresh_token')
  localStorage.removeItem('community_worker')
  next('/login')
}

router.beforeEach(async (to, from, next) => {
  if (to.path === '/login') {
    next()
    return
  }

  const token = localStorage.getItem('community_access_token')
  if (!token) {
    next('/login')
    return
  }

  if (!isTokenExpired(token)) {
    next()
    return
  }

  // Token is expired — try to refresh
  const refreshToken = localStorage.getItem('community_refresh_token')
  if (!refreshToken) {
    clearAuthAndRedirect(next)
    return
  }

  try {
    const res = await axios.post(
      `${import.meta.env.VITE_API_BASE_URL}/community/auth/refresh`,
      { refresh_token: refreshToken }
    )
    localStorage.setItem('community_access_token', res.data.access_token)
    if (res.data.refresh_token) {
      localStorage.setItem('community_refresh_token', res.data.refresh_token)
    }
    next()
  } catch {
    clearAuthAndRedirect(next)
  }
})

export default router
