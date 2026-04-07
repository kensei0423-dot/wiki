# API 参考

后端运行在 `localhost:3777`，以下是全部 API 端点。

## 认证 API

| 方法 | 路径 | 说明 | 需登录 |
|------|------|------|--------|
| POST | `/auth/register` | 注册 | 否 |
| POST | `/auth/login` | 登录 | 否 |
| POST | `/auth/logout` | 登出 | 是 |
| GET | `/auth/me` | 获取当前用户 | 否 (返回 null) |

## 支付 API

| 方法 | 路径 | 说明 | 需登录 |
|------|------|------|--------|
| POST | `/api/orders` | 创建 PayPal 订单 | 是 |
| POST | `/api/orders/:id/capture` | 捕获（完成）订单 | 是 |
| GET | `/api/client-token` | 获取 PayPal client token | 是 |
| GET | `/api/user/orders` | 获取当前用户的订单历史 | 是 |

## Vault API（支付方式管理）

| 方法 | 路径 | 说明 | 需登录 |
|------|------|------|--------|
| GET | `/api/vault/payment-tokens` | 获取已保存的支付方式 | 是 |
| DELETE | `/api/vault/payment-tokens/:id` | 删除已保存的支付方式 | 是 |

## 订阅 API

| 方法 | 路径 | 说明 | 需登录 |
|------|------|------|--------|
| POST | `/api/subscriptions` | 创建订阅 | 是 |
| PATCH | `/api/subscriptions/:id` | 更换订阅计划 | 是 |
| POST | `/api/subscriptions/:id/cancel` | 取消订阅 | 是 |

## 管理 API

| 方法 | 路径 | 说明 | 需登录 |
|------|------|------|--------|
| GET | `/api/admin/order-stats` | 获取订单统计 | 是 |
| GET | `/api/admin/users` | 获取所有用户列表 | 是 |
| GET | `/api/admin/disputes` | 查询争议列表 | 是 |
| GET | `/api/admin/disputes/:id` | 获取争议详情 | 是 |
| GET | `/api/admin/disputes/by-order/:orderId` | 按订单 ID 查争议 | 是 |

## 测试 API

| 方法 | 路径 | 说明 | 需登录 |
|------|------|------|--------|
| POST | `/api/test/create-order` | 测试创建订单错误 | 是 |
| POST | `/api/test/capture-order` | 测试捕获订单错误 | 是 |

## 静态页面

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 商城首页 (index.html) |
| GET | `/login` | 登录页 (login.html) |
| GET | `/profile` | 个人中心 (profile.html) |
| GET | `/admin` | 管理后台 (admin.html) |
| GET | `/test` | 测试页面 (test.html) |
| GET | `/sdk-test` | SDK 测试页 (sdk-test.html) |

## 请求/响应格式

- Content-Type: `application/json`
- 认证: Cookie-based session (`connect.sid`)
- 错误响应: `{ error: "message" }` + 对应 HTTP 状态码

## PayPal API 调用

后端通过原生 `fetch` 直接调用 PayPal REST API（未使用 `@paypal/paypal-server-sdk`）。

### OAuth Token

```
POST https://api-m.sandbox.paypal.com/v1/oauth2/token
Authorization: Basic base64(clientId:clientSecret)
Body: grant_type=client_credentials
```

### 幂等性

- 创建订单时附带 `PayPal-Request-Id` 头
- 30 分钟内相同 Request-Id 返回缓存结果
- `seenRequestIds` Map 在本地做去重

## 相关页面

- [[architecture]] — 系统架构
- [[payment-flows]] — 支付流程
- [[error-handling]] — 错误码
- [[testing]] — 测试端点
