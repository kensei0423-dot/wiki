# Vault 系统（支付方式保存）

## 概述

Vault 系统允许用户在首次支付时保存 PayPal 账户，后续购买无需打开 PayPal 弹窗即可完成支付。

## 工作原理

### Vault-with-Purchase（首次保存）

在 [[payment-flows#Flow 1|Flow 1]] 中，用户可勾选"保存支付方式"复选框：

```
创建订单时附带 vault 指令
→ PayPal 弹窗中用户授权 + 同意保存
→ 捕获成功后，PayPal 返回 payment_token
→ 后端保存 token 到用户的 savedPaymentMethods
```

### 免弹窗支付（后续使用）

已保存的用户走 [[payment-flows#Flow 2|Flow 2]]：

```
创建订单时附带 vault_id
→ PayPal 直接使用已保存的支付方式
→ 无需弹窗，订单自动完成
```

## 数据结构

```json
{
  "paymentTokenId": "8kk02145ab4869372",
  "customerId": "customer_1234567",
  "email": "buyer@example.com",
  "savedAt": "2025-02-24T10:30:00.000Z"
}
```

| 字段 | 说明 |
|------|------|
| paymentTokenId | PayPal 支付令牌 ID，用于后续免弹窗支付 |
| customerId | PayPal 客户 ID，用于生成 id_token |
| email | 用户的 PayPal 邮箱 |
| savedAt | 保存时间 |

## 管理操作

### 查看

- **用户侧**: 个人中心 (`/profile`) 显示已保存的支付方式
- **管理侧**: 管理后台 (`/admin`) 用户详情中查看

### 删除

```
用户点击删除 → 确认弹窗
            → DELETE /api/vault/payment-tokens/:id
            → 后端调用 PayPal Payment Tokens API 删除
            → 更新本地 users.json
            → 前端刷新列表
```

## 相关 API

| 端点 | 说明 |
|------|------|
| `GET /api/vault/payment-tokens` | 获取已保存的支付方式 |
| `DELETE /api/vault/payment-tokens/:id` | 删除已保存的支付方式 |
| `GET /api/client-token` | 用 customerId 生成 id_token（Classic SDK 用） |

## PayPal API

- **Payment Tokens API v3**: 管理 vault tokens
- **Generate Token**: 用 customer_id 生成 id_token 供 Classic SDK 使用

## 相关页面

- [[payment-flows]] — 支付流程（Flow 1 和 Flow 2）
- [[user-system]] — 用户数据模型
- [[api-reference]] — API 端点
