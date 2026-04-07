# ReelShort 支付系统概览

## 项目简介

ReelShort 是一个短视频平台，本项目是其 **支付商城系统**（ReelShort Store），集成 PayPal 实现会员订阅和虚拟币购买功能。

## 技术栈

- **前端**: 原生 HTML/CSS/JS，PayPal JS SDK v6
- **后端**: Node.js + Express (端口 3777)
- **支付**: PayPal Orders API v2 (sandbox 环境)
- **数据存储**: 内存 + JSON 文件持久化（`users.json`, `order-stats.json`）
- **会话管理**: express-session，24 小时过期

## 产品目录

| 类型 | 产品 | 价格 |
|------|------|------|
| VIP 周卡 | Weekly VIP | $19.99 |
| VIP 年卡 | Yearly VIP | $199.99 |
| 金币包 | 100 coins | $4.99 |
| 金币包 | 500 coins | $19.99 |
| 金币包 | 1000 coins | $34.99 |
| 金币包 | 2000 coins | $49.99 |
| 金币包 | 5000 coins | $79.99 |
| 金币包 | 10000 coins | $99.99 |

## 核心模块

- [[architecture]] — 系统三层架构
- [[payment-flows]] — 5 种支付流程详解
- [[user-system]] — 用户认证与数据模型
- [[admin-dashboard]] — 管理后台
- [[api-reference]] — 全部 API 端点
- [[error-handling]] — PayPal 错误码分类
- [[testing]] — 错误测试方案
- [[vault-system]] — 支付方式保存与复用

## 运行状态（截至最近数据）

- 发起订单: 140
- 成功: 97 (69.3%)
- 失败: 22 (15.7%)
- 放弃/待处理: 21 (15%)

## 源文件索引

| 文件 | 说明 |
|------|------|
| `reelshort/server.js` | 后端实现（1309 行） |
| `reelshort/index.html` | 商城前端页面 |
| `reelshort/login.html` | 登录/注册页 |
| `reelshort/admin.html` | 管理后台页面 |
| `reelshort/profile.html` | 用户个人中心 |
| `reelshort/test.html` | 错误测试页面 |
| `reelshort/payment.md` | 支付流程主文档 |
| `reelshort/server.md` | 后端设计文档 |
| `reelshort/client.md` | 前端设计文档 |
| `reelshort/user.md` | 用户系统文档 |
| `reelshort/admin.md` | 管理后台文档 |
| `reelshort/test.md` | 测试文档 |
| `reelshort/capture-order-error.md` | Capture 错误码参考 |
| `reelshort/create-order-error.md` | Create 错误码参考 |
