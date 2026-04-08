# 操作日志

## [2026-04-07] ingest | ReelShort 项目初始化

首次摄入 `reelshort/` 目录全部资料，创建 wiki：

**摄入的源文件** (14 个):
- payment.md — 支付流程主文档
- server.md — 后端设计文档
- client.md — 前端设计文档
- user.md — 用户系统文档
- admin.md — 管理后台文档
- test.md — 测试文档
- capture-order-error.md — Capture 错误码参考
- create-order-error.md — Create 错误码参考
- server.js — 后端实现 (1309 行)
- payment.pdf — 支付文档 PDF 版（早期版本）
- order-stats.json — 订单统计数据
- users.json — 用户数据
- package.json — 项目依赖
- cookies.txt — 测试会话 cookie

**生成的 wiki 页面** (9 个):
- overview.md — 项目概览
- architecture.md — 系统架构
- payment-flows.md — 支付流程
- vault-system.md — Vault 系统
- user-system.md — 用户系统
- admin-dashboard.md — 管理后台
- api-reference.md — API 参考
- error-handling.md — 错误处理
- testing.md — 测试方案

## [2026-04-08] ingest | PayPal V6 SDK Quick Start 官方文档

摄入 PayPal 官方 V6 SDK 快速集成文档（docs.paypal.ai）。

**新增页面**:
- paypal-v6-quickstart.md — 官方最小集成指南、Intent 模式、Shipping 配置、Negative Testing、上线清单、监控指标、与 ReelShort 实现对比

**更新页面** (3 个):
- architecture.md — SDK 对比表新增 V6 Quick Start 列，添加交叉引用
- payment-flows.md — 新增官方 Quick Start 对比章节，添加交叉引用
- index.md — 索引新增 paypal-v6-quickstart 条目
