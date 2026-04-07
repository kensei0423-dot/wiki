# ReelShort Wiki 索引

> 短视频平台 ReelShort 支付系统的知识库

## Wiki 页面

### 核心

| 页面 | 说明 |
|------|------|
| [[wiki/overview]] | 项目概览、技术栈、产品目录、源文件索引 |
| [[wiki/architecture]] | 三层架构、SDK 对比、数据流 |

### 支付

| 页面 | 说明 |
|------|------|
| [[wiki/payment-flows]] | 5 种支付流程详解（新用户/回头客/信用卡） |
| [[wiki/vault-system]] | 支付方式保存与免弹窗复用 |

### 系统

| 页面 | 说明 |
|------|------|
| [[wiki/user-system]] | 用户认证、数据模型、会话管理 |
| [[wiki/admin-dashboard]] | 管理后台、用户管理、争议处理 |
| [[wiki/api-reference]] | 全部 30+ API 端点参考 |

### 质量保障

| 页面 | 说明 |
|------|------|
| [[wiki/error-handling]] | PayPal 错误码分类（200+ 错误码） |
| [[wiki/testing]] | 7 个错误测试场景、幂等性测试 |

## 原始资料

位于 `reelshort/` 目录：

| 类型 | 文件 |
|------|------|
| 设计文档 | `payment.md` (主文档), `server.md`, `client.md`, `user.md`, `admin.md`, `test.md` |
| 错误参考 | `capture-order-error.md`, `create-order-error.md` |
| 实现代码 | `server.js`, `index.html`, `login.html`, `profile.html`, `admin.html`, `test.html` |
| 运行数据 | `users.json`, `order-stats.json`, `cookies.txt` |
| 其他 | `payment.pdf` (payment.md 早期版本), `payment.pptx`, `generate-pptx.js` |
