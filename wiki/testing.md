# 测试方案

## 测试页面

测试页面位于 `GET /test`（`test.html`），用于模拟 PayPal 订单错误场景。

## 两种触发方式

### Mock Header（模拟头）

通过 `PayPal-Mock-Response` 请求头注入错误：

```json
{
  "mock_application_codes": "INTERNAL_SERVER_ERROR"
}
```

**优点**: 可精确控制返回的错误类型
**缺点**: 仅在 sandbox 环境可用

### Natural Trigger（自然触发）

通过传入无效数据触发真实错误：

- 无效 token → NOT_AUTHORIZED
- 无效 order ID → RESOURCE_NOT_FOUND
- 未批准订单 → ORDER_NOT_APPROVED

**优点**: 测试真实错误路径
**缺点**: 可触发的错误类型有限

## 7 个测试场景

### Create Order 错误

| # | 场景 | 触发方式 | 错误码 |
|---|------|----------|--------|
| 1 | 服务器内部错误 | Mock Header | INTERNAL_SERVER_ERROR |
| 2 | 未授权 | Natural (无效 token) | NOT_AUTHORIZED |

### Capture Order 错误

| # | 场景 | 触发方式 | 错误码 |
|---|------|----------|--------|
| 3 | 服务器内部错误 | Mock Header | INTERNAL_SERVER_ERROR |
| 4 | 资源不存在 | Natural (无效 order ID) | RESOURCE_NOT_FOUND |
| 5 | 支付工具被拒 | Mock Header | INSTRUMENT_DECLINED |
| 6 | 交易被拒 | Mock Header | TRANSACTION_REFUSED |
| 7 | 订单未批准 | Natural (未批准订单) | ORDER_NOT_APPROVED |

## 测试端点

```
POST /api/test/create-order
POST /api/test/capture-order
```

这些端点与正式端点行为一致，但支持 Mock Header 注入。

## 幂等性测试

### PayPal-Request-Id

- 每个创建订单请求附带唯一 `PayPal-Request-Id`
- 30 分钟内相同 ID 返回缓存响应
- 用于防止重复创建订单

### 本地去重

```javascript
// seenRequestIds: Map<requestId, timestamp>
function trackInitiated(requestId) {
  const now = Date.now();
  // 清理 30 分钟前的记录
  for (const [id, time] of seenRequestIds) {
    if (now - time > 30 * 60 * 1000) seenRequestIds.delete(id);
  }
  // 已见过则跳过计数
  if (seenRequestIds.has(requestId)) return false;
  seenRequestIds.set(requestId, now);
  orderStats.initiated++;
  return true;
}
```

## 订单统计追踪

测试和正式流程共用 `orderStats`:

```json
{
  "initiated": 140,
  "success": 97,
  "failed": 22
}
```

- **initiated**: 去重后的发起数
- **success**: 捕获成功数
- **failed**: 捕获失败数
- **差额** (initiated - success - failed): 放弃/待处理订单

## 相关页面

- [[error-handling]] — 完整错误码参考
- [[payment-flows]] — 支付流程
- [[api-reference]] — 测试 API 端点
