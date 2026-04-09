---
title: PayPal 一次性支付最佳实践
source: PayPal Developer Docs
date: 2026-04-09
tags: [paypal, checkout, best-practices, one-time, conversion, buttons]
---

# PayPal 一次性支付最佳实践

一键支付方案，跳过手动填写信息，加速买家结账体验。适用于实体商品和数字商品。

## 核心理念

买家点击 PayPal 按钮后，PayPal 自动提供：
- 联系方式
- 收货地址
- 支付信息

商户无需买家手动输入，减少购物车放弃率。

## 按钮放置策略

### 上游放置（Upstream）— 推荐

在买家输入任何信息**之前**展示 PayPal 按钮，如购物车页、商品详情页。

| 放置位置 | 效果 |
|----------|------|
| 购物车页 | 买家一键结账，无需填表 |
| 商品详情页 | 快速单品购买 |
| 迷你购物车 | 减少跳转步骤 |

**最佳实践**：
- PayPal 按钮放在其他需要填写信息的结账方式**前面**
- Pay Later 消息放在订单总价附近
- 传入 `data-page-type` 参数，让 PayPal 优化按钮行为
- 商品修改选项（尺寸、颜色等）放在按钮**上方**

### 结账页放置（Checkout）

买家已手动走到结账页时：

- 识别 PayPal 用户，主动选中 PayPal 选项
- PayPal 按钮应是买家的**最后一步操作**
- 批准后直接跳转到订单成功页
- Create Order 时传入买家已填的地址和联系方式
- 设置 `shipping_preference: SET_PROVIDED_ADDRESS`（锁定地址不可改）

## 合规要求

> PayPal 用户协议要求：PayPal/Venmo 与其他支付方式**平等展示**，包括 logo 位置、支付流程和费用。不得将其他支付方式放在 PayPal 前面。

## 提升转化率

### 优化登录体验

- 如有买家邮箱，传入 Create Order 调用（预填登录页）
- Web View 中 PayPal 页面必须**全高度**展示，不能用 iframe

### 优化结账体验

| 实践 | 说明 |
|------|------|
| **Pay Now 按钮** | 买家在 PayPal 页面直接完成支付，无需返回商户站 |
| **无需额外操作** | 买家点 Pay Now 后不应再需要任何操作 |
| **传入行项目** | SKU、商品名、价格传入 Create Order，提高透明度减少争议 |
| **Shipping 回调** | 上游流程中根据买家地址计算运费和税费 |
| **App Switch** | 跳转 PayPal App 完成认证和支付 |

### Pay Now 流程

```
买家点击 PayPal 按钮
    ↓
PayPal 弹窗/App（登录 + 确认）
    ↓
买家点击 Pay Now
    ↓
Create Order + Capture（PayPal 侧完成）
    ↓
跳转回商户订单成功页
```

## Shipping 回调

物理商品**必须**集成 shipping 回调，即使只有一种配送方式：

- `onShippingAddressChange` — 买家换地址时更新运费
- `onShippingOptionsChange` — 买家换配送方式时更新金额

未集成时，PayPal 无法展示配送选项，买家必须返回商户站选择。

## 关键 API 参数

| 参数 | 用途 |
|------|------|
| `data-page-type` | 告诉 PayPal 按钮所在页面类型（cart/product/checkout） |
| `shipping_preference` | `SET_PROVIDED_ADDRESS` 锁定地址 / `GET_FROM_FILE` 用 PayPal 地址 |
| `user_action` | `PAY_NOW` 直接完成支付 / `CONTINUE` 返回商户确认 |
| `email_address` | 预填买家邮箱加速登录 |
| `line_items` | 商品明细（名称、SKU、数量、价格） |

## 相关页面

- [[paypal-checkout-integration]] — Checkout 完整集成指南
- [[negative-testing]] — Sandbox 错误模拟测试
