# 支付流程

系统支持 5 种支付流程，覆盖新用户、回头客、自定义按钮和标准按钮等场景。

## Flow 1: 新用户 — 自定义按钮 (SDK v6)

使用自定义 HTML 按钮 + PayPal JS SDK v6 headless 模式。

```
用户选择商品 → 点击自定义"Pay with PayPal"按钮
            → 前端调用 POST /api/orders 创建订单
            → SDK v6 打开 PayPal 弹窗
            → 用户登录 PayPal 并授权
            → 前端调用 POST /api/orders/:id/capture
            → 后端捕获付款，更新用户数据
            → 显示成功弹窗
```

**Vault 选项**: 用户可勾选"保存支付方式"复选框（vault-with-purchase），在支付同时保存 PayPal 账户，下次可直接使用。

## Flow 2: 回头客 — Vault ID 免弹窗

已保存支付方式的用户，无需打开 PayPal 弹窗即可完成支付。

```
用户选择商品 → 选择已保存的支付方式
            → 前端调用 POST /api/orders (带 vault_id)
            → 后端创建订单时附带 payment_source.paypal.vault_id
            → 订单自动创建为 COMPLETED 状态
            → 前端调用 POST /api/orders/:id/capture
            → 完成支付，无需弹窗
```

**优势**: 零摩擦支付体验，提高转化率。

## Flow 3: 新用户 — 标准 PayPal 按钮 (Classic SDK)

使用 PayPal 标准金色按钮。

```
用户选择商品 → 点击 PayPal 标准按钮
            → Classic SDK 创建订单 (createOrder callback)
            → PayPal 弹窗，用户授权
            → onApprove callback 触发 capture
            → 完成支付
```

## Flow 4: 回头客 — 标准按钮 + id_token

通过 Classic SDK 的 `id_token` 机制识别回头客。

```
页面加载 → 前端请求 GET /api/client-token
        → 后端用 customer_id 生成 id_token
        → Classic SDK 初始化时传入 id_token
        → PayPal 识别用户，展示已保存的支付方式
        → 用户选择已有方式或新增
        → 完成支付
```

## Flow 5: ACDC 信用卡直接输入

直接在页面上嵌入信用卡输入框，无需 PayPal 弹窗。

```
用户选择商品 → 填写卡号/到期日/CVV
            → 前端调用 POST /api/orders (payment_source: card)
            → 3DS 验证（如需要）
            → 后端 capture 订单
            → 完成支付
```

## 流程对比

| 流程 | SDK | 弹窗 | Vault | 适用 |
|------|-----|------|-------|------|
| Flow 1 | v6 | 是 | 可选 | 新用户，品牌定制 |
| Flow 2 | v6 | 否 | 必需 | 回头客，极速支付 |
| Flow 3 | Classic | 是 | 否 | 新用户，快速集成 |
| Flow 4 | Classic | 是 | 自动 | 回头客，标准按钮 |
| Flow 5 | v6 | 否 | 否 | 信用卡直付 |

## Vault（支付方式保存）系统

### 保存的数据结构

```json
{
  "paymentTokenId": "xxx",
  "customerId": "xxx",
  "email": "user@example.com",
  "savedAt": "2025-02-24T..."
}
```

### 管理操作

- **查看**: 个人中心和管理后台均可查看已保存的支付方式
- **删除**: 确认弹窗 → 调用 PayPal Payment Tokens API 删除 → 更新本地数据
- **使用**: 选择已保存方式后直接下单，走 Flow 2

## 订阅管理

- **更换计划**: 周卡 ↔ 年卡切换
- **取消订阅**: 二次确认 + 2% 留存优惠
- **续费**: 周卡自动续费享 5% 折扣

## 相关页面

- [[architecture]] — 系统架构
- [[error-handling]] — 支付错误处理
- [[api-reference]] — API 端点
- [[testing]] — 错误测试
