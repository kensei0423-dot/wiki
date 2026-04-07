# 管理后台

管理后台位于 `/admin`，提供用户管理和 PayPal 争议处理功能。

## 功能概览

### 顶部统计栏

| 指标 | 数据来源 |
|------|----------|
| Total Users | `users.json` 用户数量 |
| Total Revenue | 所有成功订单金额总和 |
| Active VIP | 当前有效 VIP 用户数 |
| Saved Payment Methods | 已保存支付方式总数 |

### Tab 1: Users（用户管理）

**搜索/过滤**:
- 按用户名搜索
- 按 PayPal 邮箱搜索
- 按 Payment Token ID 搜索
- 按 Customer ID 搜索

**用户详情面板**:
- **PayPal Info** — 关联的 PayPal 账户信息
- **Saved Methods** — 已保存的支付方式列表
- **Transactions** — 交易历史

### Tab 2: Disputes（争议管理）

**三种搜索模式**:

1. **By Order ID** — 输入订单 ID，系统通过 order → capture IDs → disputes 链路查找关联争议
2. **By Case ID** — 输入 PayPal 争议案例 ID（格式: `PP-D-12345`）
3. **By Transaction ID** — 输入交易 ID 查找争议

**争议列表**:
- 按日期范围过滤
- 按状态过滤
- 争议详情弹窗（720px 宽）

**争议详情弹窗显示**:
- 争议 ID、状态、原因
- 交易信息（金额、日期）
- 买家/卖家信息
- 争议消息记录
- 本地用户匹配（通过 captureId 和 order ID 与 `users.json` 交叉引用）

## PayPal API 集成

| API | 用途 |
|-----|------|
| Customer Disputes API v1 | 查询和管理争议 |
| Orders API v2 | 查询订单详情，获取 capture IDs |

### Sandbox 特殊处理

PayPal sandbox 的 `end_time` 过滤有时不生效，后端在本地做额外的日期过滤。

## 订单统计

- 来源: `order-stats.json`
- 三个计数器: initiated / success / failed
- 幂等去重: `seenRequestIds` Map + 30 分钟窗口

## 相关页面

- [[overview]] — 项目概览
- [[user-system]] — 用户数据模型
- [[api-reference]] — 管理 API 端点
- [[error-handling]] — 错误码参考
