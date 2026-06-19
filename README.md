# EZLove 易挂念

社区老人关爱管理平台，连接家庭与社区，让牵挂被看见。

## 项目结构

```
ezlove/
├── frontend/          # 微信小程序端（uni-app + Vue 3）
│   └── src/           # 子女端 + 长辈端小程序
├── admin-frontend/    # 社区管理后台（Vue 3 + Element Plus）
│   └── src/           # 社区工作人员 Web 管理界面
├── backend/           # 后端 API（FastAPI + PostgreSQL）
│   ├── app/           # API、模型、服务、工具
│   ├── alembic/       # 数据库迁移
│   └── tests/         # 测试
└── docker-compose.yml # 容器编排
```

## 快速开始

### 前置要求

- Docker & Docker Compose
- Node.js 18+（前端开发）
- Python 3.10+（后端开发）

### 1. 配置环境变量

```bash
cp backend/.env.example backend/.env
# 编辑 backend/.env，填写以下必填项：
#   DATABASE_URL - 数据库连接字符串
#   JWT_SECRET   - JWT 签名密钥（生成方法：python -c "import secrets; print(secrets.token_hex(32))"）
```

### 2. 启动服务

```bash
# 启动数据库和 Redis
docker compose up -d db redis

# 运行数据库迁移
cd backend && alembic upgrade head

# 初始化管理员账号（首次运行）
python seed_community.py --password YOUR_SECURE_PASSWORD

# 启动后端
uvicorn app.main:app --reload --port 8001
```

### 3. 前端开发

```bash
# 社区管理后台
cd admin-frontend && npm install && npm run dev

# 微信小程序
cd frontend && npm install && npm run dev:mp-weixin
```

## 功能模块

### 家庭端（微信小程序）
- 子女发送关怀动态（文字 + 图片）
- 长辈查看动态、已读确认、表情回应
- 已读未读追踪 + 超时预警
- AI 内容建议生成

### 社区管理端（Web 后台）
- 社区看板：老人分级统计、活跃热力图
- 老人档案管理：A/B/C 分级管理
- 食堂数据：文本/Excel 录入 + AI 解析
- 事件中心：自动预警 + 手动记录 + 处理流转

## 老人分级标准

| 级别 | 描述 |
|------|------|
| A 级 | 无自理能力，可能有认知障碍 |
| B 级 | 独居，儿女不在身边，认知正常 |
| C 级 | 老两口在一起，可协助照顾 A 级老人 |

## 技术栈

- **后端**: FastAPI, SQLAlchemy 2.0, PostgreSQL 16, Redis 7
- **小程序**: uni-app, Vue 3, uview-plus
- **管理后台**: Vue 3, Element Plus, Pinia, Axios
- **AI**: Anthropic Claude API
