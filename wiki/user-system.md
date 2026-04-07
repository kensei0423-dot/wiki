# 用户系统

## 用户数据模型

```json
{
  "username": "test1",
  "passwordHash": "<SHA-256 hash>",
  "coins": 0,
  "bonus": 0,
  "vipStatus": null,
  "orders": [],
  "savedPaymentMethods": [],
  "createdAt": "2025-02-24T..."
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| username | string | 3-20 字符 |
| passwordHash | string | SHA-256 哈希 |
| coins | number | 金币余额 |
| bonus | number | 赠送金币 |
| vipStatus | object/null | VIP 状态（类型、到期日） |
| orders | array | 订单历史 |
| savedPaymentMethods | array | 已保存的 PayPal 支付方式 |
| createdAt | string | 注册时间 |

## 认证流程

### 注册
```
POST /auth/register
Body: { username: "user1", password: "abc123" }
→ 验证用户名 3-20 字符，密码 6+ 字符
→ SHA-256 哈希密码
→ 创建用户，写入 users.json
→ 自动登录（设置 session）
```

### 登录
```
POST /auth/login
Body: { username: "user1", password: "abc123" }
→ 查找用户，比对哈希
→ 设置 req.session.user
→ 返回用户信息
```

### 会话配置

- **Cookie 名**: `connect.sid`
- **Secret**: `reelshort-demo-secret-2024`
- **有效期**: 24 小时
- **HttpOnly**: 是
- **Secure**: 否（开发环境）

### 认证中间件

`requireAuth` 中间件检查 `req.session.user`，未登录返回 401。

## 页面

### 登录页 (`/login`)
- 居中卡片式布局
- 登录/注册模式切换
- 暗色主题

### 个人中心 (`/profile`)
- 用户头像
- 余额卡片：金币 + 赠送金币 + VIP 徽章
- 订单历史表格（日期、产品、金额、状态）
- 已保存的支付方式列表

## 支付与用户的关联

支付流程通过 session 的 `pendingProductId` 将商品与用户关联：

```
用户选择商品 → session.pendingProductId = productId
           → 创建 PayPal 订单
           → 捕获成功后，根据 productId 更新用户余额/VIP
           → 清除 pendingProductId
```

## 测试账户

| 用户名 | 密码 | 说明 |
|--------|------|------|
| test1 | abc123 | 预置测试账户 |
| test2 | abc123 | 预置测试账户 |

## 数据持久化

用户数据存储在 `users.json`，服务启动时加载，每次变更后写入磁盘。

## 相关页面

- [[overview]] — 项目概览
- [[payment-flows]] — 支付流程（用户如何购买）
- [[admin-dashboard]] — 管理员视角的用户管理
- [[api-reference]] — 认证相关 API
