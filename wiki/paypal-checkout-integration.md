---
title: PayPal Checkout 集成指南
source: PayPal Developer Docs
date: 2026-04-09
tags: [paypal, checkout, integration, buttons, sdk, orders-api]
---

# PayPal Checkout 集成指南

完整的 PayPal Checkout 集成流程，涵盖前端按钮、后端 API、自定义处理和测试上线。

## 架构概览

```
前端 (index.html + app.js)          后端 (Server SDK)
┌───────────────────────┐          ┌──────────────────────┐
│ PayPal Buttons 组件    │──创建──▶│ ordersCreate (Orders) │
│ createOrder callback  │          │                      │
│ onApprove callback    │──捕获──▶│ ordersCapture (Orders)│
└───────────────────────┘          └──────────────────────┘
                                            │
                                   PayPal REST API (sandbox/live)
```

## 1. 前端集成

### 引入 SDK

```html
<script src="https://www.paypal.com/sdk/js?client-id=YOUR_CLIENT_ID&components=buttons&currency=USD"></script>
```

参数说明：
- `client-id` — 必填，PayPal 应用凭证
- `components` — 可选：buttons, marks, card-fields
- `currency` — 默认 USD
- `buyer-country` — **仅 Sandbox 测试用**，生产环境不可用

### 渲染按钮

```javascript
paypal.Buttons({
  createOrder: (data, actions) => {
    // 调用后端创建订单，返回 order ID
  },
  onApprove: (data, actions) => {
    // 调用后端捕获支付
  }
}).render('#paypal-button-container');
```

### 按钮样式配置（可选）

| 属性 | 选项 |
|------|------|
| shape | `rect`（默认）, `pill` |
| color | `gold`（默认）, `blue`, `silver`, `white`, `black` |
| layout | `vertical`（默认）, `horizontal` |
| label | `paypal`, `checkout`, `buynow`, `pay` |

### Shipping 回调（可选）

- `onShippingAddressChange` — 买家更换地址时触发
- `onShippingOptionsChange` — 买家更换配送方式时触发

### Contact Module（可选）

控制买家在 PayPal 结账页是否可编辑联系信息：

| 偏好 | 说明 |
|------|------|
| `NO_CONTACT_INFO`（默认） | 隐藏联系信息 |
| `UPDATE_CONTACT_INFO` | 买家可添加/修改联系方式 |
| `RETAIN_CONTACT_INFO` | 买家可查看但不可修改 |

## 2. 后端集成

### SDK 控制器

| 控制器 | API |
|--------|-----|
| Orders Controller | Orders API v2 — 创建和捕获订单 |
| Payments Controller | Payments API v2 — 退款等操作 |

### 配置

- 服务端口：**8080**
- 环境变量：`PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`
- 默认连接 Sandbox API

### Step 1: 生成 Access Token

SDK 自动通过 OAuth 2.0 Client Credentials 获取 token。

### Step 2: 创建订单

```
POST /v2/checkout/orders
Intent: CAPTURE 或 AUTHORIZE
```

### Step 3: 捕获支付

```
POST /v2/checkout/orders/{order_id}/capture
```

## 3. App Switch（可选）

允许买家跳转到 PayPal App 完成支付后返回。

**前端**：设置 `appSwitchWhenAvailable: true`

**后端**：Create Order 时传入 `experience_context.app_switch_preference`：
- `return_url` — 买家完成后返回的页面
- `cancel_url` — 买家取消后返回的页面
- 两个 URL 必须相同，且与按钮所在页面一致

## 4. 错误处理

| 场景 | 处理方式 |
|------|----------|
| 通用错误 | `onError` 回调，显示通用错误信息 |
| 资金失败 (`INSTRUMENT_DECLINED`) | 重启支付流程，让买家选择其他支付方式 |
| 买家取消 | 显示取消确认页 |
| 退款 | 调用 Payments API 退款给买家 |

## 5. 测试

### PayPal 支付测试

1. 点击 PayPal 按钮
2. 用 **个人** Sandbox 账户登录
3. 确认金额 → 点击 Pay Now
4. 用 **商户** Sandbox 账户确认收款（扣除手续费）

### 信用卡测试

1. 用 PayPal 信用卡生成器生成测试卡号
2. 填写卡号/到期日/CVV/姓名/地址
3. 提交订单
4. 商户 Sandbox 账户确认收款

## 6. 上线清单

- [ ] PayPal Developer Dashboard 登录商户账户
- [ ] 获取 **Live** 凭证（Client ID + Secret）
- [ ] 替换代码中的 Sandbox 凭证为 Live 凭证
- [ ] 更新 API 端点（sandbox → live）
- [ ] 测试真实小额交易

## 相关页面

- [[negative-testing]] — Sandbox 错误模拟测试
- [[one-time-payments]] — 一次性支付最佳实践
