---
title: PayPal V6 SDK Quick Start
source: PayPal Developer Docs (docs.paypal.ai)
date: 2026-04-08
tags: [paypal, sdk, v6, integration, quickstart]
---

# PayPal V6 SDK Quick Start Integration

最小代码量接入 PayPal 支付。适用于 PoC、基础电商结账或简单捐赠表单。

## 核心流程

1. **创建订单** (Create Order) — 服务端调用 Orders API v2
2. **买家批准** (Buyer Approval) — 前端 SDK 渲染按钮，用户点击支付
3. **捕获支付** (Capture Payment) — 服务端捕获资金

## 前提条件

- PayPal 开发者账户 + Client ID & Secret
- （可选）Sandbox 账户启用 Negative Testing：Dashboard → Sandbox → Accounts → View/Edit → Enable Negative Testing

## 项目结构（Node.js）

```
paypal-minimal/
├── .env              # 环境变量（Client ID、Secret）
├── server.js         # Express 后端
├── public/
│   └── index.html    # 前端（SDK v6 按钮）
└── package.json
```

依赖：`express`、`@paypal/checkout-server-sdk`、`dotenv`

## 后端关键代码

### 创建订单

```javascript
app.post('/api/orders', async (req, res) => {
  const request = new paypal.orders.OrdersCreateRequest();
  request.requestBody({
    intent: 'CAPTURE',
    purchase_units: [{
      amount: { currency_code: 'USD', value: req.body.amount || '10.00' }
    }]
  });
  const order = await client.execute(request);
  res.json({ id: order.result.id });
});
```

### 捕获订单

```javascript
app.post('/api/orders/:orderID/capture', async (req, res) => {
  const request = new paypal.orders.OrdersCaptureRequest(req.params.orderID);
  const capture = await client.execute(request);
  res.json({ id: capture.result.id, status: capture.result.status });
});
```

## 前端关键代码（SDK v6）

```javascript
const sdkInstance = await window.paypal.createInstance({
  clientId: "YOUR_CLIENT_ID",
  components: ["paypal-payments"]
});

const eligibility = await sdkInstance.findEligibleMethods();
if (eligibility.isEligible('paypal')) {
  const paypalButton = document.createElement('paypal-button');
  document.querySelector('#paypal-button-container').append(paypalButton);

  const paypalCheckoutSession = await sdkInstance.createPayPalOneTimePaymentSession({
    onApprove, onCancel, onError
  });

  paypalButton.addEventListener("click", async () => {
    const createOrderPromise = createOrder();  // 不要 await
    await paypalCheckoutSession.start(
      { presentationMode: "auto" },
      createOrderPromise
    );
  });
}
```

SDK 脚本：`https://www.sandbox.paypal.com/web-sdk/v6/core`

## 环境配置

```bash
# .env 文件
# Sandbox（开发）
PAYPAL_CLIENT_ID=your_sandbox_client_id
PAYPAL_CLIENT_SECRET=your_sandbox_secret
NODE_ENV=development

# Production（生产） — 上线时切换
# PAYPAL_CLIENT_ID=your_production_client_id
# PAYPAL_CLIENT_SECRET=your_production_secret
# NODE_ENV=production
```

## Intent 模式

| Intent | 说明 | 适用场景 |
|--------|------|----------|
| `CAPTURE` | 买家批准后立即扣款 | 即时交付的商品/服务 |
| `AUTHORIZE` | 先授权，后扣款（29 天有效） | 需要确认库存/发货后再扣款 |

## Shipping 配置

| shipping_preference | 说明 |
|---------------------|------|
| `GET_FROM_FILE`（默认） | 使用买家 PayPal 账户中的地址 |
| `SET_FROM_PROVIDER` | 商户提供地址，买家不可编辑 |
| `NO_SHIPPING` | 数字商品，无需物流地址 |

ReelShort 作为数字内容平台，应使用 `NO_SHIPPING`。

## Negative Testing（错误模拟）

仅 Sandbox 环境可用。通过 `PayPal-Mock-Response` header 触发：

| 错误场景 | 错误码 | 预期结果 |
|----------|--------|----------|
| 余额不足 | `INSUFFICIENT_FUNDS` | 捕获时失败 |
| 支付方式被拒 | `INSTRUMENT_DECLINED` | 捕获时失败 |
| 服务器错误 | `INTERNAL_SERVER_ERROR` | 创建/捕获时 500 |
| 交易被拒 | `TRANSACTION_REFUSED` | 捕获时失败 |
| 重复发票 | `DUPLICATE_INVOICE_ID` | 创建时失败 |

## 上线清单

- [ ] Sandbox 测试所有场景
- [ ] .env 切换到 Production 配置
- [ ] 前端 Client ID 切换到生产
- [ ] 配置 HTTPS 证书
- [ ] 用 $1 真实交易测试
- [ ] 确认 PayPal 账户收到资金

## 上线后监控指标

| 指标 | 目标 | 低于目标时的处理 |
|------|------|-----------------|
| 支付成功率 | 95% | 检查 API 错误日志 |
| 取消率 | <20% | 优化结账 UX 和价格展示 |
| 错误率 | <2% | 检查错误日志和 API 响应 |
| 创建订单响应时间 | <2s | 优化服务器性能 |
| 捕获响应时间 | <3s | 检查服务器性能 |

## 与 ReelShort 现有实现的对比

| 特性 | 官方 Quick Start | ReelShort 实现 |
|------|-----------------|----------------|
| SDK 版本 | v6 | v6 + Classic 双模式 |
| 按钮 | `<paypal-button>` Web Component | 自定义 HTML 按钮（headless） |
| Vault | 未包含 | 支持 vault-with-purchase |
| 错误处理 | 基础 try/catch | 7 大类 120+ 错误码 |
| 数据存储 | 无 | JSON 文件持久化 |
| 订阅 | 未包含 | VIP 周卡/年卡 |

## 多语言支持

官方 Quick Start 支持 Node.js、Python、Java、PHP、Ruby、cURL。ReelShort 当前使用 Node.js。

## 相关页面

- [[architecture]] — 系统架构和 SDK 选型
- [[payment-flows]] — 5 种支付流程详解
- [[error-handling]] — 完整错误码参考
- [[testing]] — 测试方案（含 Negative Testing）
- [[api-reference]] — API 端点列表
