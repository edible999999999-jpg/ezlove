# EZLove 易挂念生产落地方案

> 版本：1.0  
> 日期：2026-08-11  
> 部署边界：阿里云中国内地，最多 1 台弹性云服务器  
> 目标：以单社区政府试点为第一阶段，在 8-12 周内完成可审核、可试运行、可运维的生产版本

## 1. 决策摘要

采用“单台 ECS 承载计算与数据库，阿里云 OSS 承载媒体，阿里云百炼承载 AI”的方案。

- ECS 内运行：Nginx、FastAPI、PostgreSQL 16、Redis 7、管理后台、定时任务和备份任务。
- OSS 存放：用户原始图片、生成图片、生成视频、海报和数据库加密备份。
- AI 使用阿里云百炼华北 2（北京）业务空间，文本、视觉理解、图像编辑和视频生成均在中国内地区域调用。
- 微信端使用一个小程序承载子女、老人和志愿者角色；政府项目方负责提供合法主体、认证小程序、域名、备案资料、隐私文本和类目资质。
- 首期只使用 1 个备案主域名和 2 个业务子域名：`api.<主域名>`、`admin.<主域名>`。可选增加 `static.<主域名>` 绑定 OSS，自定义域名总数最多 3 个。
- 不采用 Supabase 托管版，也不在 ECS 自托管完整 Supabase。现有 PostgreSQL + SQLAlchemy 架构直接上线，降低跨境、资源和运维风险。

本方案不是高可用架构。单机故障时业务会中断，因此把自动备份、监控告警和 4 小时内恢复作为强制验收项。

## 2. 项目方必须解决的前置条件

以下事项由政府项目方或其指定运营公司完成，技术承建方提供材料模板和配置协助，但不能代替主体承担责任。

| 类别 | 项目方交付物 | 阻塞范围 |
|---|---|---|
| 主体 | 政府/事业单位/公司主体及经办人授权 | 小程序注册、认证、备案、云账号 |
| 微信小程序 | 已认证账号、AppID、AppSecret、管理员与体验成员 | 微信登录、订阅消息、审核发布 |
| 小程序类目 | 与社区养老、生活服务实际业务匹配的类目及所需资质 | 提审与发布 |
| 域名 | 完成实名认证且主体一致的可备案域名 | HTTPS API、管理后台、小程序合法域名 |
| 备案 | ICP 备案；上线后按要求完成公安联网备案；是否需要 App 备案由项目方和接入商确认 | 中国内地公网访问 |
| 隐私合规 | 隐私政策、用户协议、个人信息处理规则、第三方 SDK 清单、撤回/注销渠道 | 小程序审核、正式运营 |
| 数据授权 | 老人、家属、社区工作者数据来源与授权边界，尤其是手机号、地址、健康备注和告警记录 | 数据导入与生产试点 |
| 内容与 AI | AI 服务使用规则、生成内容标识规则、人工审核责任人、禁用场景 | AI 功能开放 |
| 微信消息 | 订阅消息模板 ID 及实际模板字段 | 未读提醒和告警通知 |

阿里云明确要求中国内地服务器上的互联网服务完成 ICP 备案；网站开通后还应在规定时间内完成公安联网备案。备案资料、时长和前置审批以主体所在省通信管理局及阿里云控制台当期要求为准。

## 3. 单服务器生产架构

```text
微信小程序 ───────┐
                  ├── HTTPS ──> api.example.cn ──┐
管理后台 ─────────┘                              │
                                                 ▼
┌──────────────────── 阿里云 ECS ──────────────────────────┐
│ Nginx :443                                                │
│   ├─ /api/*  -> FastAPI (2 workers)                       │
│   └─ admin.example.cn -> Vue 静态文件                      │
│                                                          │
│ FastAPI                                                   │
│   ├─ PostgreSQL 16：业务数据                              │
│   ├─ Redis 7：缓存、限流、短任务状态                       │
│   └─ APScheduler：未读检查、告警和清理                     │
│                                                          │
│ backup job：pg_dump -> AES 加密 -> OSS                    │
└──────────────────────────────────────────────────────────┘
          │                     │                   │
          ▼                     ▼                   ▼
   阿里云 OSS              阿里云百炼           微信开放 API
  图片/视频/备份         LLM/图片/视频          登录/订阅消息
```

### 3.1 ECS 规格

推荐生产规格：

- 8 vCPU、16 GiB RAM，Alibaba Cloud Linux 3 或 Ubuntu 22.04 LTS。
- 系统盘 ESSD 100 GiB；独立 ESSD 数据盘 200 GiB，挂载 PostgreSQL 数据目录。
- 固定公网 IP 或 EIP，公网带宽 5-10 Mbps 起步。
- 安全组仅开放 22、80、443；22 只允许运维固定 IP，数据库和 Redis 不映射到公网。
- Docker Engine + Compose v2；所有镜像固定版本，不使用 `latest`。

最低可运行规格为 4 vCPU、8 GiB，但不建议同时开启 AI 媒体任务轮询、报表导出和批量导入。若只能购买 4C8G，FastAPI 限制为 2 个 worker，PostgreSQL `shared_buffers` 设为 1 GiB，并限制 AI 并发为文本 5、图片 2、视频 1。

### 3.2 容器与资源上限

| 服务 | 建议内存上限 | 说明 |
|---|---:|---|
| PostgreSQL | 4 GiB | 数据持久化到独立数据盘 |
| FastAPI | 3 GiB | 2-4 workers，健康检查与优雅重启 |
| Redis | 512 MiB | 开启密码和 AOF，`maxmemory-policy allkeys-lru` |
| Nginx + 管理后台 | 512 MiB | TLS、静态文件、反向代理 |
| 监控/日志代理 | 1 GiB | 可使用阿里云云监控插件或轻量代理 |
| 系统余量 | 7 GiB | 文件处理、备份、突发任务 |

### 3.3 数据库选择

正式方案使用本机 PostgreSQL 16。

- 现有代码已经使用 SQLAlchemy 2.0 async、asyncpg 和 Alembic，无需迁移 ORM。
- Supabase 托管版没有中国大陆托管区域，不作为政府项目默认数据底座。
- 自托管完整 Supabase 官方建议 4 核 8GB 以上，还会增加 Kong、Auth、Realtime、Storage、Studio 等容器；本项目已有认证、API 和存储层，引入后收益小、单机风险高。
- 若未来允许增加托管资源，优先迁移阿里云 RDS PostgreSQL，而不是改写为 Supabase。

## 4. 域名、证书和网络

### 4.1 域名数量

必需：1 个备案主域名，2 个子域名。

| 域名 | 用途 | 微信后台配置 |
|---|---|---|
| `api.example.cn` | FastAPI、上传、SSE Agent | request 合法域名、uploadFile 合法域名、downloadFile 合法域名 |
| `admin.example.cn` | 社区管理后台 | 不需要配置到小程序 |
| `static.example.cn`（可选） | OSS 图片/视频自定义域名 | downloadFile 合法域名；如客户端直传则加入 uploadFile |

表中的 `example.cn` 是部署占位符，实施时必须整体替换为项目方完成实名认证和备案的真实主域名。

不需要为数据库、Redis、百炼、微信 API 单独购买域名。它们分别通过 Docker 内网或供应商域名访问。

### 4.2 HTTPS 与安全组

- 使用阿里云数字证书管理服务或受信任 CA 证书，覆盖 `api`、`admin`，可使用通配符证书。
- 强制 HTTPS，TLS 1.2+；80 仅做 301 跳转。
- Nginx 设置上传大小、超时、SSE 不缓存；AI 视频提交接口快速返回任务 ID，禁止保持数分钟 HTTP 长连接。
- PostgreSQL 5432、Redis 6379、FastAPI 容器端口只在 Docker 网络开放，删除当前 Compose 中的公网端口映射。
- 后台管理端增加 IP 白名单或 VPN 是推荐项；至少开启 MFA、强密码、登录失败锁定和操作审计。

## 5. 微信小程序与用户信息

### 5.1 主体责任边界

代码不能绕过主体和用户授权。项目方需要在微信公众平台完成主体认证，技术方只接入主体提供的 AppID/AppSecret。未取得主体、类目和隐私审核前，只能发布体验版，不能承诺正式上线。

### 5.2 获取信息的正确方式

| 信息 | 获取方式 | 是否静默 | 本项目用途 |
|---|---|:---:|---|
| `openid`、`session_key` | 小程序 `wx.login` 获取 code，后端调用 `jscode2session` | 是 | 建立账号和登录态 |
| 昵称 | 用户主动输入，或经授权后获取微信提供的能力 | 否 | 家庭展示、社区档案 |
| 头像 | 用户主动选择头像或上传 | 否 | 展示，可首期不收集 |
| 手机号 | 用户点击带 `getPhoneNumber` 能力的按钮，后端用动态 code 换取 | 否 | 告警联系、社区工作；非核心流程不得强制 |
| 地址/健康备注 | 社区工作人员在有业务授权的情况下录入 | 否 | 关怀服务；属于高敏感业务字段 |
| 图片/视频 | 用户主动选择并上传 | 否 | 发送牵挂、AI 生成输入 |
| 订阅消息授权 | 每次在明确业务场景调用 `requestSubscribeMessage` | 否 | 未读提醒、告警通知 |

现有代码只完成了 `wx.login -> jscode2session -> openid -> JWT`。没有发现手机号授权接入；昵称与角色目前依赖用户后续填写。正式上线前必须新增手机号动态 code 的后端换取流程，或明确首期完全不采集手机号。

### 5.3 最小必要原则

- 首次进入只获取 `openid`，不强制昵称、头像和手机号。
- 用户进入“绑定老人”“接收电话告警”等确需手机号的功能时，再解释目的并请求授权。
- 老人端默认不展示风险分、健康备注或社区内部标签；家属端只展示其绑定关系内的数据。
- AI 请求不得默认发送手机号、完整地址、身份证号、健康备注等直接标识信息。Agent 工具返回给 LLM 前使用内部 ID，并按角色裁剪字段。
- 提供账号注销、关系解绑、数据导出/更正、撤回授权和删除上传媒体的入口。
- 隐私政策列明微信、阿里云、OSS、百炼和短信服务等第三方处理者以及数据用途、范围、保存期限和联系方式。

## 6. AI 方案

### 6.1 统一供应商与区域

首期统一采用阿里云百炼华北 2（北京）业务空间，避免再引入境外 LLM 和多套密钥。百炼提供 OpenAI 兼容接口，现有 `AsyncOpenAI` 封装可通过修改 `LLM_BASE_URL`、`LLM_API_KEY` 和 `LLM_MODEL` 接入。

推荐环境变量：

```dotenv
LLM_PROVIDER=aliyun_bailian
LLM_API_KEY=<DASHSCOPE_API_KEY>
LLM_BASE_URL=https://<WorkspaceId>.cn-beijing.maas.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus
BAILIAN_WORKSPACE_ID=<WorkspaceId>
BAILIAN_API_BASE=https://<WorkspaceId>.cn-beijing.maas.aliyuncs.com/api/v1
OSS_BUCKET=<private-bucket>
OSS_ENDPOINT=oss-cn-beijing.aliyuncs.com
```

模型 ID 会随平台更新。生产发布时在百炼控制台锁定一个已验证版本或快照，不自动追随“latest”；文档中的 `qwen-plus`、`wan2.7-image` 和 `wan2.7-i2v` 是首选族，不是永久锁定的版本号。

### 6.2 AI 功能与具体 API

| 功能 | 首选模型/服务 | API | 当前代码状态 | 上线级别 |
|---|---|---|---|---|
| 暖心文案建议 | `qwen-plus` | `POST .../compatible-mode/v1/chat/completions` | 已实现，需配置并强化 JSON 解析 | P0 |
| 食堂文本解析 | `qwen-plus` | 同上，要求 JSON Schema/结构化输出 | 已实现 LLM 解析链路 | P0 |
| 图片理解与配文 | 支持视觉输入的千问 VL 模型，以控制台可用型号为准 | OpenAI 兼容 Chat Completions，多模态消息 | 已实现 base64 图片输入，但默认 `qwen-plus` 未必支持视觉，必须拆分模型配置 | P0 |
| 社区 Agent | `qwen-plus` 或工具调用验证更稳定的千问型号 | OpenAI 兼容 Chat Completions `tools`/function calling | 已实现 7 个工具和最多 5 轮调用 | P0 只读；写工具 P1 |
| 老照片增强 | `wan2.7-image` 或万相通用图像编辑 | `POST .../api/v1/services/aigc/multimodal-generation/generation`；旧编辑接口为异步任务 | 只有 503 占位代码 | P1 |
| 照片生成短视频 | `wan2.7-i2v` | `POST .../api/v1/services/aigc/video-generation/video-synthesis`，再 `GET .../api/v1/tasks/{task_id}` | 只有 503 占位代码 | P1 |
| AI 生成内容审核 | 阿里云内容安全服务，或项目方指定审核服务 | 文本/图片/视频检测 API | 未接入 | P0 文本和上传图片；P1 视频 |

### 6.3 文本生成链路

1. 小程序调用 `POST /api/v1/ai/suggest`。
2. 后端按用户角色、时间和可选上下文构造提示词；不得拼入无关个人信息。
3. 调用百炼 OpenAI 兼容 `chat/completions`，请求超时 15 秒，最多重试 1 次。
4. 使用 JSON Schema 或 Pydantic 校验输出，拒绝任意非结构化 JSON；当前直接 `json.loads` 的实现需要加固。
5. 经过文本安全审核后返回 3 条建议。
6. 用户必须确认或编辑后才能发送；AI 不能自动代用户向老人发送消息。
7. 模型不可用时返回仓库内置文案，并记录 `fallback=true`。

### 6.4 图片与视频生成链路

1. 客户端向后端申请上传凭证，图片直传私有 OSS；首期也可经 API 上传，但最终必须转存 OSS。
2. 后端创建 `ai_media_tasks` 记录，保存用户、输入对象 key、模型、状态、积分预扣和幂等键。
3. 调用百炼异步生成 API，保存供应商 `task_id` 后立即返回 `202 Accepted`。
4. 单机定时任务每 5-10 秒轮询，使用 Redis 锁防止重复处理；禁止使用常驻 Celery 集群。
5. 成功后在结果 URL 失效前下载并转存私有 OSS，执行内容审核并写入输出对象 key。
6. 客户端轮询本系统 `GET /api/v1/ai/media/tasks/{id}`，通过 10 分钟有效的 OSS 签名 URL 展示结果。
7. 失败、超时或审核拒绝时自动退还积分；同一幂等键不能重复扣费。

现有媒体接口缺少任务表、供应商调用、轮询、OSS 转存、内容审核和任务查询接口，不能仅填写 `VIDEO_GEN_API_KEY` 就上线。

### 6.5 Agent 的 LLM 与边界

当前 Agent 已实现这些工具：

- `query_inactive_elders`
- `get_building_summary`
- `get_elder_status`
- `get_today_alerts`
- `list_unconfirmed_elders`
- `confirm_elder_active`
- `get_weekly_trend`

正式上线的控制要求：

- P0 只开放 6 个只读工具。`confirm_elder_active` 会写入社区事件，必须改为“生成确认卡片 -> 工作人员二次确认 -> 后端写入”，不得由 LLM 一步执行。
- 每个工具继续强制绑定 `worker.community_id`，并增加 RBAC；LLM 传入的社区 ID、用户 ID 一律不可信。
- Agent 最多 5 轮工具调用、单次最多 20 秒、单用户每分钟最多 10 次、单日 token 配额可配置。
- 对话历史首期不长期保存；保留请求 ID、工作者 ID、工具名、参数摘要、结果条数、模型版本、token 和错误码 180 天用于审计。日志不记录完整手机号和健康备注。
- Agent 回答必须显示“AI 辅助，不作为安全确认或医疗判断”；所有风险结论来源于规则与实时业务数据，LLM 只负责查询编排和解释。
- 禁止 Agent 自动发订阅消息、短信、删除数据、修改老人等级或关闭告警。
- 首期不需要 RAG。只有项目方提供经过审批的制度文件后，再增加知识库；业务实时数据仍通过受控工具查询，不能向量化全量个人信息。

## 7. 外部 API、账号和密钥清单

### 7.1 必需 API

| 提供方 | API/资源 | 凭据 | 用途 |
|---|---|---|---|
| 微信 | `sns/jscode2session` | AppID、AppSecret | 登录换取 openid/session_key |
| 微信 | `cgi-bin/token` | AppID、AppSecret | 获取服务端 access_token |
| 微信 | `message/subscribe/send` | access_token、模板 ID | 未读与告警订阅消息 |
| 微信 | 手机号获取服务端接口 | access_token、动态 code | 可选手机号授权 |
| 阿里云百炼 | OpenAI 兼容 Chat Completions | 业务空间 API Key、Workspace ID | 文案、解析、Agent、视觉理解 |
| 阿里云 OSS | Put/Get Object、签名 URL | RAM AccessKey 或 ECS RAM Role | 媒体与备份 |
| 阿里云内容安全 | 文本/图片/视频审核 | RAM 权限 | UGC/AIGC 内容审核 |
| 阿里云 DNS/证书 | DNS、SSL 证书 | 阿里云账号/RAM | 域名解析和 HTTPS |

### 7.2 P1 API

| 提供方 | API/资源 | 用途 |
|---|---|---|
| 百炼万相图像 | 图像生成/编辑 | 老照片增强、可选海报背景 |
| 百炼万相视频 | 图生视频提交与任务查询 | 照片动画化、短视频生成 |
| 阿里云短信 | SendSms | 家属或工作人员的兜底告警；需签名和模板审核 |
| 阿里云云监控 | 主机、进程、磁盘和 URL 监控 | 运维告警 |

### 7.3 密钥管理

- AppSecret、JWT_SECRET、数据库密码、百炼 API Key 和 OSS 凭据只保存在服务器环境或阿里云 KMS/凭据管家，不提交 Git。
- 优先给 ECS 绑定 RAM 角色访问 OSS，避免长期 AccessKey。
- 项目方、开发、测试和生产使用不同微信小程序/环境、数据库、OSS 前缀和百炼 Key。
- 每 90 天轮换可轮换密钥；发生人员离场或泄露时立即轮换。

## 8. 现有代码上线缺口

### P0：不完成不能生产试点

1. 生产 Compose：去除数据库、Redis、后端公网端口；增加 Nginx、健康检查、资源限制、日志轮转、只读文件系统和自动重启。
2. OSS：替换本地 `static/uploads` 和 `static/ai_media` 长期存储，数据库只存 object key，不存永久公网 URL。
3. 微信：生产 AppID、合法域名、隐私接口声明、订阅消息模板；决定是否实现手机号授权。
4. AI：拆分 `TEXT_MODEL`、`VISION_MODEL`、`AGENT_MODEL`；统一超时、重试、结构化输出、成本与调用审计。
5. Agent：写操作二次确认、RBAC、字段脱敏、Redis 限流、输入长度和历史条数限制。
6. 安全：管理后台登录锁定/MFA、CSRF 或等效保护、严格 CORS、上传恶意文件扫描、OSS 私有桶、依赖和镜像扫描。
7. 数据：生产迁移演练、种子数据与真实数据隔离、备份恢复演练、数据保存和删除策略。
8. 监控：CPU、内存、磁盘、容器、PostgreSQL、HTTP 5xx、任务积压、AI 失败率和证书到期告警。
9. 测试：微信真机主流程、老人端无障碍、权限隔离、告警定时任务、断网/超时/AI 降级、备份恢复。
10. 合规：用户协议、隐私政策、第三方清单、AI 标识与人工复核、账号注销和数据删除。
11. 修复已确认代码缺陷：`ai_media.py` 的视频生成端点引用未定义的 `point_service`；Redis 当前没有持久卷和密码；`/health` 只检查 `ANTHROPIC_API_KEY`，不能反映 `LLM_API_KEY`/百炼可用性。
12. 修复 AI 隐私与稳定性问题：Agent 的老人状态工具当前可能把 `health_notes` 直接送入 LLM；文本生成当前直接 `json.loads` 且吞掉全部异常。上线前必须最小化字段、记录分类错误并区分超时、限流、审核拒绝和解析失败。

### P1：试运行后 2-4 周

1. 接入老照片增强、图生视频及异步任务表。
2. 接入短信兜底和内容安全视频审核。
3. 增加对象生命周期、媒体缩略图和可选 CDN。
4. 完成等保定级咨询和差距整改；是否需二级或更高等级由项目方及主管部门确认。

## 9. 备份、恢复和运维

### 9.1 备份策略

- 每日 02:00 执行 `pg_dump --format=custom`，AES-256 加密后上传 OSS。
- 每周执行一次完整备份校验；每日备份保留 30 天，每月最后一份保留 12 个月，最终期限由项目方数据制度确认。
- OSS 开启版本控制、服务端加密和生命周期规则；备份账号只有写入指定前缀和读取恢复前缀的最小权限。
- 每月在隔离数据库执行一次恢复演练并记录 RTO/RPO。
- 目标 RPO 24 小时；目标 RTO 4 小时。若要求分钟级 RPO 或无停机，单 ECS 约束无法满足，必须增加 RDS/备机。

### 9.2 监控与告警

告警发送给至少两名运维人员：

- CPU > 85% 持续 10 分钟；内存 > 90%；数据盘 > 80%。
- API 5xx 比例 > 2% 持续 5 分钟；健康检查连续 3 次失败。
- PostgreSQL 连接使用率 > 80%；备份失败；证书 30 天内到期。
- AI 文本失败率 > 10%；视频任务超过 15 分钟；OSS 上传失败率 > 5%。

## 10. 分阶段实施计划

### 第 0 阶段：主体与云资源，预计 2-4 周，可与开发并行

- 项目方完成主体、阿里云账号、域名、ECS、OSS、百炼业务空间和小程序认证。
- 提交 ICP 备案，准备小程序类目与隐私材料。
- 决定手机号是否属于首期必要信息。

验收：AppID/AppSecret、备案域名、ECS、OSS 私有桶、百炼北京 Key 和模板申请单均有明确负责人。

### 第 1 阶段：生产底座，预计 1-2 周

- 完成生产 Compose、Nginx、HTTPS、安全组、环境密钥和 OSS。
- 完成数据库迁移、备份、监控和恢复演练。

验收：公网只开放 80/443/受限 22；数据库和 Redis 无公网端口；从 OSS 备份恢复到空库成功。

### 第 2 阶段：核心业务与微信，预计 2 周

- 接入正式微信登录、订阅消息、合法域名和隐私声明。
- 完成家庭绑定、发送、查看、已读、告警和社区处理闭环。
- 完成角色越权与真机测试。

验收：至少 20 组模拟家庭连续运行 7 天，核心流程成功率 >= 99%，无跨家庭/跨社区数据泄露。

### 第 3 阶段：文本 AI 与 Agent，预计 1-2 周

- 接入百炼文本/视觉模型、结构化输出、内容审核、调用审计和降级。
- Agent P0 只读上线，写操作保留人工二次确认。

验收：200 条文案/解析测试结构化成功率 >= 98%；Agent 权限测试全部通过；供应商不可用时核心业务不受影响。

### 第 4 阶段：试运行与审核，预计 2 周

- 50-100 名真实试点用户灰度，逐步扩到 100-500 名老人。
- 完成培训、值班表、故障预案、用户反馈和小程序提审。

验收：连续 14 天无 P0 故障；告警闭环可追溯；备份、恢复、注销和数据删除均演练通过。

### 第 5 阶段：AI 媒体，预计 2-4 周，P1 可独立延期

- 接入老照片增强和图生视频异步任务。
- 小流量灰度，设置每人/每日配额和总预算熔断。

验收：生成失败自动退款；结果完成后 5 分钟内转存 OSS；违规内容不下发；预算达到 80%/100% 时告警/停用。

## 11. 成本口径

具体价格受地域、购买时长、带宽、模型版本和采购折扣影响，正式采购前以阿里云控制台询价为准。预算表应分为：

- 固定成本：8C16G ECS、200GB ESSD 数据盘、固定公网带宽、域名、证书（可用免费证书但需管理续期）。
- 用量成本：OSS 存储/请求/外网流量、短信、百炼 token、图像张数、视频秒数、内容审核次数。
- 人工成本：开发整改、备案材料、测试、运维值班、内容审核和用户支持。

必须在后台配置三层 AI 预算：单用户日限额、单功能并发限额、项目月度金额上限。视频生成默认不开启，待项目方确认预算后灰度。

## 12. 上线验收红线

以下任一项不满足，不发布正式版：

- 主体、备案、类目、隐私政策或用户授权材料缺失。
- 数据库、Redis 或管理端调试接口暴露公网。
- 无成功的备份恢复演练，或备份与生产机在同一磁盘。
- 微信登录、家庭/社区权限存在越权漏洞。
- AI 可以未经用户确认自动发送内容，或 Agent 可以未经二次确认执行写操作。
- 用户上传和 AI 输出没有审核、举报和删除通道。
- 没有明确故障联系人、告警渠道和 4 小时恢复流程。

## 13. 参考资料

- [阿里云 ICP 备案流程](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/icp-filing-application-overview)
- [阿里云 ICP 备案服务器要求](https://help.aliyun.com/zh/icp-filing/basic-icp-service/user-guide/overview)
- [阿里云百炼 OpenAI 兼容接口](https://help.aliyun.com/zh/model-studio/first-api-call-to-qwen)
- [阿里云百炼平台与北京地域 Endpoint](https://help.aliyun.com/zh/model-studio/what-is-model-studio)
- [万相图像生成与编辑 API](https://help.aliyun.com/en/model-studio/wan-image-generation-and-editing-api-reference)
- [万相图生视频 API](https://help.aliyun.com/en/model-studio/image-to-video-general-api-reference)
- [Supabase 自托管资源要求](https://supabase.com/docs/guides/self-hosting/docker)
- [微信小程序登录](https://developers.weixin.qq.com/miniprogram/dev/api/open-api/login/wx.login.html)
- [微信小程序手机号能力](https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/getPhoneNumber.html)
- [微信小程序网络与服务器域名](https://developers.weixin.qq.com/miniprogram/dev/framework/ability/network.html)

## 14. 最终责任分工

| 角色 | 负责内容 |
|---|---|
| 政府项目方 | 主体、预算、数据合法来源、业务制度、类目与前置资质、最终验收 |
| 运营主体 | 小程序认证、隐私政策、用户服务、内容审核、投诉和注销处理 |
| 技术承建方 | 代码整改、部署、数据安全措施、AI 接入、测试、监控、备份和运维文档 |
| 阿里云 | ECS/OSS/百炼等云产品可用性及其责任边界内的安全能力 |
| 社区工作人员 | 老人档案授权录入、异常核实、Agent 写操作人工确认和处置留痕 |

项目上线负责人应维护一份带姓名、截止时间和证据链接的交付清单。主体问题由项目方解决，但未解决前必须在项目计划中标记为正式发布阻塞项。
