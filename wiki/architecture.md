# 系统架构

## 三层架构

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│   Frontend   │────▶│  Backend (Express)│────▶│  PayPal API  │
│  index.html  │◀────│  server.js:3777   │◀────│  (sandbox)   │
└─────────────┘     └──────────────────┘     └─────────────┘
```

### 1. 前端层

- **商城页** (`index.html`) — 产品展示、PayPal 支付按钮、成功弹窗
- **登录页** (`login.html`) — 登录/注册切换、居中卡片式布局
- **个人中心** (`profile.html`) — 头像、余额卡片（金币+VIP）、订单历史
- **管理后台** (`admin.html`) — 用户管理、争议处理
- **测试页** (`test.html`) — PayPal 错误模拟
- **UI 风格**: 暗色主题，响应式布局

### 2. 后端层

- **框架**: Express.js (Node 18+，使用原生 fetch)
- **端口**: 3777
- **会话**: express-session，24 小时 cookie
- **数据持久化**:
  - `users.json` — 用户数据（注册信息、订单、保存的支付方式）
  - `order-stats.json` — 订单统计（initiated/success/failed）
- **认证**: SHA-256 密码哈希（演示级别）
- **中间件**: `requireAuth` 拦截未登录请求

### 3. PayPal API 层

- **环境**: Sandbox（沙盒测试）
- **主要 API**:
  - Orders API v2 — 创建和捕获订单
  - Payment Tokens API v3 — Vault（保存支付方式）
  - Subscriptions API v1 — 订阅管理
  - Customer Disputes API v1 — 争议查询
- **认证**: OAuth 2.0 Client Credentials
- **幂等性**: PayPal-Request-Id + 30 分钟去重窗口

## PayPal SDK 对比

| 特性 | SDK v6 (主用) | Classic SDK |
|------|--------------|-------------|
| 按钮样式 | 自定义 HTML 按钮 | PayPal 标准金色按钮 |
| 触发方式 | Headless，代码触发 | 点击 PayPal 按钮 |
| Vault 支持 | vault-with-purchase | id_token |
| 适用场景 | 品牌一致性要求高 | 快速集成 |

## 数据流

```
用户点击购买 → 前端调用 /api/orders (创建订单)
            → PayPal 弹窗，用户授权
            → 前端调用 /api/orders/:id/capture (捕获付款)
            → 后端更新用户余额/VIP 状态
            → 前端显示成功弹窗
```

## 相关页面

- [[overview]] — 项目概览
- [[payment-flows]] — 详细支付流程
- [[api-reference]] — API 端点列表
