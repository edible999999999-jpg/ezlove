<template>
  <div class="login-page">
    <!-- Left: Brand Panel -->
    <div class="brand-panel">
      <div class="brand-content">
        <div class="brand-logo">
          <div class="logo-icon">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <path d="M24 4C14 4 8 12 8 20c0 6 4 10 8 13v7a2 2 0 002 2h12a2 2 0 002-2v-7c4-3 8-7 8-13C40 12 34 4 24 4z" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/>
              <path d="M18 30h12M18 34h12" stroke="rgba(255,255,255,0.4)" stroke-width="1.5" stroke-linecap="round"/>
              <circle cx="24" cy="18" r="5" fill="rgba(255,255,255,0.2)" stroke="rgba(255,255,255,0.6)" stroke-width="1.5"/>
              <path d="M24 16v4M22 18h4" stroke="rgba(255,255,255,0.8)" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </div>
        </div>
        <h1 class="brand-title">易挂念</h1>
        <p class="brand-subtitle">社区关爱管理平台</p>
        <p class="brand-desc">让关心自然流动，让牵挂被看见。<br/>连接家庭与社区，守护每一位长者。</p>
      </div>
      <div class="brand-decoration">
        <div class="deco-circle deco-circle--1"></div>
        <div class="deco-circle deco-circle--2"></div>
        <div class="deco-circle deco-circle--3"></div>
      </div>
    </div>

    <!-- Right: Login Form -->
    <div class="form-panel">
      <div class="form-container animate-fade-in-up">
        <div class="form-header">
          <h2 class="form-title">欢迎回来</h2>
          <p class="form-hint">请登录您的社区管理账号</p>
        </div>

        <el-form ref="formRef" :model="form" :rules="rules" @submit.prevent="handleLogin" class="login-form">
          <el-form-item prop="phone">
            <el-input
              v-model="form.phone"
              placeholder="请输入手机号"
              size="large"
              :prefix-icon="Phone"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码"
              size="large"
              show-password
              :prefix-icon="Lock"
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleLogin"
              class="login-btn"
            >
              {{ loading ? '登录中...' : '登 录' }}
            </el-button>
          </el-form-item>
        </el-form>

        <div class="form-footer">
          <span class="form-footer-text">需要帮助？联系系统管理员</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { Phone, Lock } from '@element-plus/icons-vue'

const userStore = useUserStore()
const loading = ref(false)
const formRef = ref(null)
const form = reactive({ phone: '', password: '' })

const rules = {
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1\d{10}$/, message: '请输入正确的11位手机号', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' },
  ],
}

async function handleLogin() {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
  } catch {
    return
  }
  loading.value = true
  try {
    await userStore.login(form.phone, form.password)
  } catch (e) {
    // error handled in request interceptor
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.login-page {
  min-height: 100vh;
  display: flex;
}

// — Brand Panel —
.brand-panel {
  flex: 0 0 44%;
  background: linear-gradient(160deg, $dark-hearth 0%, $brand-terracotta-dark 60%, $brand-terracotta 100%);
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  padding: $sp-10;
}

.brand-content {
  position: relative;
  z-index: 2;
  text-align: center;
  animation: fadeInUp 0.8s $ease-out both;
}

.logo-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  height: 80px;
  border-radius: $radius-xl;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  margin-bottom: $sp-6;
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.brand-title {
  font-family: $font-display;
  font-size: $fs-4xl;
  font-weight: $fw-bold;
  color: #fff;
  letter-spacing: 0.08em;
  margin-bottom: $sp-2;
}

.brand-subtitle {
  font-family: $font-body;
  font-size: $fs-lg;
  color: rgba(255, 255, 255, 0.75);
  font-weight: $fw-medium;
  margin-bottom: $sp-8;
}

.brand-desc {
  font-size: $fs-base;
  color: rgba(255, 255, 255, 0.5);
  line-height: $lh-relaxed;
  max-width: 280px;
  margin: 0 auto;
}

// — Decorative Circles —
.brand-decoration {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.deco-circle {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.06);

  &--1 {
    width: 400px;
    height: 400px;
    top: -100px;
    right: -80px;
    background: radial-gradient(circle, rgba(199, 92, 58, 0.15) 0%, transparent 70%);
    animation: float 20s ease-in-out infinite;
  }
  &--2 {
    width: 260px;
    height: 260px;
    bottom: -60px;
    left: -40px;
    background: radial-gradient(circle, rgba(212, 162, 78, 0.1) 0%, transparent 70%);
    animation: float 15s ease-in-out infinite reverse;
  }
  &--3 {
    width: 160px;
    height: 160px;
    top: 40%;
    right: 15%;
    background: radial-gradient(circle, rgba(107, 143, 113, 0.1) 0%, transparent 70%);
    animation: float 12s ease-in-out infinite;
  }
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(10px, -15px) scale(1.02); }
  66% { transform: translate(-8px, 10px) scale(0.98); }
}

// — Form Panel —
.form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: $warm-cream;
  padding: $sp-10;
}

.form-container {
  width: 100%;
  max-width: 380px;
}

.form-header {
  margin-bottom: $sp-10;
}

.form-title {
  font-family: $font-display;
  font-size: $fs-3xl;
  font-weight: $fw-bold;
  color: $text-primary;
  margin-bottom: $sp-2;
}

.form-hint {
  font-size: $fs-md;
  color: $text-secondary;
}

.login-form {
  .el-form-item {
    margin-bottom: $sp-5;
  }
}

.login-btn {
  width: 100%;
  height: 48px;
  font-size: $fs-md;
  font-weight: $fw-semibold;
  letter-spacing: 0.08em;
  border-radius: $radius-sm;
}

.form-footer {
  margin-top: $sp-8;
  text-align: center;
}

.form-footer-text {
  font-size: $fs-sm;
  color: $text-placeholder;
}

// — Responsive —
@media (max-width: 900px) {
  .brand-panel {
    display: none;
  }
  .form-panel {
    padding: $sp-6;
  }
}
</style>
