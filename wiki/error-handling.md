# 错误处理

PayPal Orders API v2 的错误码完整分类，涵盖创建订单和捕获订单两个阶段。

## 错误分类体系

两个阶段共用以下 7 大类错误：

### 1. PayPal 服务器/系统错误

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| INTERNAL_SERVER_ERROR | PayPal 内部错误 | 重试 |
| SERVICE_UNAVAILABLE | 服务暂时不可用 | 稍后重试 |

### 2. 认证/权限错误

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| NOT_AUTHORIZED | 未授权 | 检查凭证 |
| PERMISSION_DENIED | 权限不足 | 检查 API 权限 |
| CONSENT_NEEDED | 需要用户同意 | 引导用户授权 |

### 3. 买家/付款方账户错误

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| INSTRUMENT_DECLINED | 支付工具被拒 | 提示用户换一种支付方式 |
| PAYER_ACCOUNT_LOCKED_OR_CLOSED | 付款方账户被锁定 | 提示联系 PayPal |
| PAYER_CANNOT_PAY | 付款方无法支付 | 提示用户检查账户 |

### 4. 商户/收款方账户错误

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| PAYEE_ACCOUNT_NOT_SUPPORTED | 收款账户不支持 | 检查商户账户配置 |
| PAYEE_ACCOUNT_NOT_VERIFIED | 收款账户未验证 | 验证商户账户 |

### 5. 风控/反欺诈错误

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| TRANSACTION_REFUSED | 交易被风控拒绝 | 联系 PayPal 或换方式 |
| COMPLIANCE_VIOLATION | 合规违规 | 联系 PayPal 支持 |

### 6. 订单状态错误（仅 Capture 阶段）

| 错误码 | 说明 | 处理建议 |
|--------|------|----------|
| ORDER_NOT_APPROVED | 订单未被用户批准 | 等待用户在弹窗中批准 |
| ORDER_ALREADY_CAPTURED | 订单已被捕获 | 检查是否重复提交 |
| RESOURCE_NOT_FOUND | 订单不存在 | 检查订单 ID |

### 7. 参数/请求验证错误

这是最大的一类，包含多个子类：

**请求格式**:
- INVALID_JSON_POINTER_FORMAT
- INVALID_PARAMETER_SYNTAX

**缺失参数**:
- MISSING_REQUIRED_PARAMETER

**无效值**:
- INVALID_PARAMETER_VALUE
- INVALID_CURRENCY_CODE
- INVALID_COUNTRY_CODE

**金额不匹配**（仅 Create 阶段）:
```
amount = item_total + tax_total + shipping + handling + insurance
         - shipping_discount - discount
```
- AMOUNT_MISMATCH — 金额计算不等式不成立

**Vault 相关错误**:
- INVALID_VAULT_ID
- VAULT_INSTRUCTION_REQUIRED

**存储凭证错误**:
- INVALID_STORED_CREDENTIAL
- NETWORK_TOKEN_REQUEST_FAILED

## 错误码数量

| 阶段 | 错误码数量 |
|------|-----------|
| Create Order | ~120+ |
| Capture Order | ~80+ |

## 前端错误处理策略

1. **可重试错误** (INTERNAL_SERVER_ERROR) → 自动重试 1-2 次
2. **用户操作错误** (INSTRUMENT_DECLINED) → 提示用户换支付方式
3. **配置错误** (NOT_AUTHORIZED) → 记录日志，展示通用错误
4. **状态错误** (ORDER_NOT_APPROVED) → 引导用户完成授权

## 相关页面

- [[payment-flows]] — 支付流程
- [[testing]] — 错误测试方案
- [[api-reference]] — API 端点

## 源文件

- `reelshort/create-order-error.md` — Create 阶段完整错误码
- `reelshort/capture-order-error.md` — Capture 阶段完整错误码
