# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# EZLove — 易挂念

## 项目概览

微信小程序，让子女通过分享日常来守护独居老人。核心机制：子女发送牵挂内容 → 老人查看 → 系统追踪已读状态 → 未读时提醒子女。

- 前端：uni-app (Vue 3 Composition API + Vite) + Pinia + uview-plus
- 后端：FastAPI + PostgreSQL (asyncpg) + Redis + Alembic + APScheduler
- 部署：Docker Compose + 阿里云 ECS

## 语言与沟通

- 所有人机交互使用中文
- 代码中的注释如需添加也用中文
- commit message 使用英文

---

## 产品策略（影响所有技术决策）

1. **老人端零学习成本** —— 老人只需点微信聊天中的小程序卡片即可查看内容，不需要学会打开小程序。所有老人端页面必须大字体（≥36rpx）、高对比度、单列布局。
2. **牵挂而非监控** —— 产品传达的是家人关心，不是被监控。界面文案、推送措辞一律从"关心"角度出发，禁止出现"监控"、"追踪"、"报警"等冷冰冰的词汇。
3. **已读即在线** —— 系统通过老人查看内容的行为来判断是否在线，这是核心检测机制。view_events 表是产品骨架。
4. **AI 辅助不替代** —— AI 生成内容建议供子女选择确认，不直接发送给老人。

---

## 开发命令

```bash
# 前端
cd frontend
npm run dev:h5                 # H5 开发模式 (localhost:5173)
npm run dev:mp-weixin          # 微信小程序开发模式
npm run build:h5               # H5 生产构建
npm run build:mp-weixin        # 微信小程序生产构建

# 后端（先确保 .env 存在，参照 backend/.env.example）
cd backend
uvicorn app.main:app --reload  # 开发模式 (localhost:8001)
alembic upgrade head           # 执行数据库迁移
alembic revision --autogenerate -m "desc"  # 生成迁移脚本

# 基础设施（端口避开 ezpr：PG=5433, Redis=6380, Backend=8001）
docker-compose up -d db redis  # 仅启动数据库和缓存
docker-compose up -d           # 启动全部

# 健康检查
curl http://localhost:8001/health
```

---

## 架构要点

### 认证流程

- **微信登录**：`uni.login` → 前端拿 code → `POST /api/v1/auth/wx-login` → 后端 code 换 openid → 返回 JWT
- **开发登录**：`POST /api/v1/auth/dev-login`（仅 `DEBUG=true`）
- **老人端静默授权**：老人打开小程序卡片时自动获取 openid，无需手动登录

### 核心业务流

```
子女发送牵挂 → care_moments 表
                  ↓
老人打开查看 → view_events 表（自动记录 openid + 时间 + 时长）
                  ↓
定时检测 → 未读超时 → alerts 表 → 通知子女
```

### API 路由前缀映射

所有路由挂在 `/api/v1` 下：

| 域 | 后端前缀 | 前端页面目录 |
|---|---|---|
| 认证 | `/auth` | `pages/login/` |
| 用户 | `/users` | `pages/profile/` |
| 绑定关系 | `/relations` | `pages/bind/` |
| 牵挂内容 | `/moments` | `pages/send/`, `pages/view/` |
| 告警 | `/alerts` | `pages/alerts/` |
| AI生成 | `/ai` | `pages/send/ai-suggest` |
| 社区联系人 | `/community-contacts` | `pages/elder/` |

---

## 目录结构约束

### 前端 `frontend/src/`

- `api/` — 按域拆分的 HTTP 请求模块，所有请求通过 `request.js` 封装
- `components/` — 通用组件
- `composables/` — 可复用组合式函数
- `pages/` — 按功能域分目录
- `stores/` — Pinia stores，按域拆分
- `styles/` — 全局 SCSS

**规则：**
1. 每新增一个 `pages/xxx/` 必须同步创建对应的 `api/xxx.js` 和 `stores/xxx.js`
2. 页面文件单文件不超过 300 行
3. 老人端页面（`pages/view/`）字体 ≥ 36rpx，按钮触控区域 ≥ 96rpx

### 后端 `backend/app/`

- `api/v1/` — 路由层
- `models/` — SQLAlchemy ORM，一文件一表
- `schemas/` — Pydantic 请求/响应 schema
- `services/` — 业务逻辑层
- `tasks/` — APScheduler 定时任务（告警检测）
- `utils/` — 工具模块（微信SDK、AI调用）

**规则：**
1. API 路由层只做参数校验和 HTTP 处理，业务逻辑下沉到 `services/`
2. 每个域完整四层：model → schema → service → api
3. 新增 model 必须在 `models/__init__.py` 中 import

---

## 开发规范

### 前端

- 使用 `<view>/<text>` 而非 `<div>/<span>`
- 使用 `uni.*` 而非 `wx.*`
- 颜色和间距使用 SCSS 变量，禁止硬编码
- 状态管理通过 Pinia store，页面不直接调 api

### 后端

- 所有数据库操作使用 async/await
- 敏感配置通过 `.env` 注入
- 错误处理使用 FastAPI HTTPException

---

## 设计系统

- 主色：`#FF8C42`（暖橙，牵挂与温暖）
- 辅助色：`#FFD166`（暖黄）
- 安全色：`#06D6A0`（绿色，已读/在线）
- 警告色：`#EF476F`（红粉，未读/告警）
- 背景色：`#FFF8F0`（暖白）
- 文字主色：`#333333`
- 圆角：卡片 24rpx，按钮 48rpx
- 老人端字体：正文 ≥ 36rpx，标题 ≥ 44rpx
