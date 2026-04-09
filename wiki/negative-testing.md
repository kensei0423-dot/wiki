---
title: PayPal Negative Testing
source: PayPal Developer Docs (developer.paypal.com)
date: 2026-04-09
tags: [paypal, testing, sandbox, negative-testing, error-simulation]
---

# PayPal Negative Testing（错误模拟测试）

在 Sandbox 环境中强制触发特定错误条件，验证错误处理逻辑是否正确。

> Beta 功能，仅限 Sandbox 环境。

## 前提条件

- **仅 Sandbox 环境** — 不能在生产环境模拟错误
- **Classic PayPal API 2.4+**
- **Business 账户**（非个人账户）

## 启用步骤

1. 登录 [developer.paypal.com](https://developer.paypal.com)
2. Dashboard → Sandbox → **Accounts**
3. 找到 Business 账户 → 点击 `...` → **View/Edit Account**
4. 切换到 **Settings** 标签
5. 将 **Negative Testing** 设为 **On**

未启用时，Sandbox 只会在正常交易流程中触发真实错误，不会强制模拟。

## 可模拟的错误类型

| 类型 | 说明 |
|------|------|
| API 调用错误 | 调用 PayPal API 时返回的错误响应 |
| Virtual Terminal / DoDirectPayment 错误 | 验证和信用卡校验错误 |

错误进一步分为：
- **与交易金额相关的错误** — 通过特定金额触发
- **与交易金额无关的错误** — 通过 Mock Header 或测试值触发

## 两种测试方法

### 1. Request Headers 方式

通过 `PayPal-Mock-Response` 请求头模拟错误：

```bash
curl -X POST https://api-m.sandbox.paypal.com/v2/checkout/orders \
  -H "PayPal-Mock-Response: {\"mock_application_codes\": \"INTERNAL_SERVER_ERROR\"}" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  -d '...'
```

常用 Mock 错误码：
- `INTERNAL_SERVER_ERROR` — 服务器内部错误
- `INSTRUMENT_DECLINED` — 支付方式被拒
- `TRANSACTION_REFUSED` — 交易被拒
- `INSUFFICIENT_FUNDS` — 余额不足
- `DUPLICATE_INVOICE_ID` — 重复发票号

### 2. Test Values 方式

通过传入特定测试值（如金额、卡号）触发对应错误。

## 适用场景

- 验证前端错误提示是否正确显示
- 测试重试逻辑（如服务器错误后自动重试）
- 确认不同错误码的降级处理（换支付方式、联系客服等）
- CI/CD 集成测试中模拟支付失败

## 注意事项

- 必须先在 Sandbox Business 账户中启用 Negative Testing
- 生产环境**无法**使用此功能
- Mock Header 方式更灵活，推荐优先使用

## 相关页面

- [[paypal-checkout-integration]] — PayPal Checkout 完整集成指南
