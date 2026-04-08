# PayPal 本地完整演示版 · CLAUDE.md

> 与生产版功能完全对等，只替换了基础设施层。
> 无需数据库、Redis、服务器、HTTPS、监控等第三方服务。

---

## 本地化替换对照表

| 生产环境 | 本地演示替换 | 影响 |
|---------|------------|------|
| PostgreSQL | `db.json` 文件 | 功能完全相同，无并发安全 |
| Redis / BullMQ | `setImmediate` 内存处理 | 功能相同，重启后队列清空 |
| HTTPS 证书 | HTTP 本地运行 | 无影响（iOS 需配置 NSAllowsLocalNetworking）|
| ngrok（Webhook） | `scripts/simulate-webhook.js` 本地脚本 | 功能相同，手动触发 |
| Webhook 签名验证 | ⚠️ 跳过（演示说明即可） | 安全性降低，不影响流程展示 |
| Sentry / Datadog | `console.log` 终端输出 | 功能相同，无告警推送 |
| 服务器部署 | `node server.js` 本地启动 | 无影响 |
| 对账定时任务 | 手动运行 `node scripts/reconcile.js` | 功能相同，手动触发 |
| 压力测试 | 跳过 | 演示不需要 |
| CI/CD | 跳过 | 演示不需要 |
| Apple Pay Face ID | Sandbox Mock Token | 演示流程完整，无需真实设备 |
| Fastlane OTP 短信 | Sandbox 固定输入 `111111` | 完整演示流程 |

---

## 包含的完整功能

```
支付方式：
  ✅ PayPal 钱包（Buttons）
  ✅ 信用卡直输（ACDC / CardFields）
  ✅ Apple Pay（Sandbox Mock）
  ✅ BNPL / Pay Later（分期）
  ✅ PLM（分期提示消息）
  ✅ Venmo（美国区）

高级功能：
  ✅ Vault（保存支付方式，存 db.json）
  ✅ Fastlane（加速结账，OTP 用 111111）
  ✅ 订阅 / 定期扣款（Subscriptions API）
  ✅ 折扣 / 优惠码（本地验证）
  ✅ 多币种支持（JPY/TWD 零精度处理）
  ✅ 争议处理（Webhook 模拟脚本触发）
  ✅ 预授权支付（intent=AUTHORIZE）
  ✅ 充值钱包（db.json 余额表）
  ✅ iOS 外链支付（localhost 联调）
  ✅ 退款（全额 + 部分）
```

---

## 需要提前开通的 Sandbox 权限

以下功能需要在 PayPal Sandbox Dashboard 手动开通（免费）：

```
□ ACDC（CardFields 信用卡直输）
□ Vault（支付方式保存）
□ Fastlane（需先开通 ACDC）
开通位置：developer.paypal.com → Apps & Credentials → 选择 App → Advanced options
```

Apple Pay 需要额外：
```
□ Apple Developer 账号（$99/年）配置 Merchant ID
□ 或：使用演示模式（Mock Token，跳过真实 Apple Pay）
```

---

## Claude Code 执行规则

### 启动时必做
1. 读取 `progress.json`
2. 找到 `in_progress` 或第一个 `pending` 步骤继续执行
3. 打印当前进度后开始

### 所有步骤完成后必做（自动测试）

当 `progress.json` 中所有步骤状态均为 `done` 时，**必须自动执行以下流程**：

```
步骤一：确认服务正在运行
  检查 http://localhost:3000 是否可访问
  若未运行 → 自动执行 node server.js &（后台启动）
  等待 2 秒确认启动成功

步骤二：运行完整测试套件
  node scripts/auto-test.js

步骤三：读取报告并输出摘要
  cat test-reports/latest.json
  展示：总计 / 通过 / 失败 / 通过率 / 各套件结果

步骤四：更新 progress.json
  加入 test_result 字段记录测试结果：
  {
    "test_result": {
      "status": "PASS" 或 "FAIL",
      "passed": N,
      "failed": N,
      "passRate": "XX%",
      "reportPath": "test-reports/latest.md",
      "runAt": "ISO时间"
    }
  }

步骤五：若有失败用例
  逐一分析失败原因
  修复代码后重新运行 node scripts/auto-test.js
  直到全部通过再结束

步骤六：自动化测试全部通过后，打印手动测试引导
  auto-test.js 会自动输出手动测试清单，包含：
  - 必须完成的测试项（带「← 必须」标记）
  - 可选测试项（附带跳过条件说明）
  - 未在向导中选择的功能自动跳过

步骤七：读取 test-reports/manual-test-todo.json
  告知用户：
  「自动化测试已完成，请按以下清单逐项手动测试。
    详细步骤见 tests/manual-test-checklist.md。
    完成后告诉我，我会更新测试报告。」
  然后等待用户反馈

步骤八：用户反馈手动测试结果后
  根据用户反馈，调用：

  node scripts/generate-final-report.js \
    --pass MT-01,MT-02,MT-04,MT-07,MT-08,MT-09 \
    --skip MT-03,MT-05,MT-10,MT-11

  参数说明：
    --pass  通过的测试项 ID（逗号分隔）
    --fail  失败的测试项 ID
    --skip  跳过的测试项 ID

  脚本会生成 test-reports/final-report-latest.md（自动化 + 手动合并）
  然后更新 progress.json 的 test_result 字段
```

### 禁止行为
- ❌ 不询问任何确认
- ❌ 不安装 PostgreSQL / Redis / Docker
- ❌ 不配置 HTTPS / 服务器 / CI/CD
- ❌ 不在测试未通过时宣布项目完成

---

## 首次使用：运行初始化向导

```bash
# 第一步：运行向导（16 题，约 3 分钟）
node scripts/init-wizard.js
```

向导会询问业务场景、支付方式、高级功能，然后生成：
- `progress.json`：只包含你需要的步骤
- `wizard-result.json`：前端标签页和后端接口的按需渲染配置

```
问题覆盖：
  第一部分（Q1-Q8）：应用类型、付款模式、退款政策、争议处理、
                     多币种、税费、折扣、用户身份
  第二部分（Q9-Q11）：端（Web/iOS）、支付方式、目标地区
  第三部分（Q12-Q16）：Vault、Fastlane、PLM、iOS 商品类型、发票
```

---

## 快速启动（向导之后）

```bash
npm install
cp .env.example .env.local
# 填写 .env.local 的 PayPal Sandbox Client ID & Secret
node server.js
# 访问 http://localhost:3000
```

---

## 文档目录结构

```
payment_local/
├── CLAUDE.md                      ← 总入口（你在这里）
├── progress.json                  ← 执行进度
├── db.json                        ← 本地数据库（自动生成）
├── .env.example                   ← 环境变量模板
│
├── tasks/
│   ├── 01-local-setup.md          ← 环境配置 + db-local.js
│   ├── 02-backend-core.md         ← 核心接口（Buttons + 退款）
│   ├── 03-backend-advanced.md     ← 高级接口（Vault/订阅/折扣等）
│   ├── 04-frontend-demo.md        ← 完整演示页面（所有支付方式）
│   ├── 05-ios-local.md            ← iOS 本地联调
│   └── 06-webhook-sim.md          ← Webhook 模拟测试
│
├── knowledge-base/
│   ├── local-vs-production.md     ← 本地版与生产版差异说明
│   ├── sandbox-guide.md           ← Sandbox 账号与测试卡号
│   ├── feature-activation.md      ← 各功能 Sandbox 开通步骤
│   └── troubleshooting.md         ← 常见问题
│
├── docs/
│   └── api-endpoints.md           ← 完整接口文档
│
├── tests/
│   └── manual-test-checklist.md  ← 手动测试清单（11 个场景）
│
├── scripts/
│   ├── init-wizard.js             ← 初始化向导（16 题）
│   ├── auto-test.js               ← 自动化测试（26 个用例）+ 手动测试引导
│   ├── generate-final-report.js  ← 生成最终完整报告（自动化 + 手动）
│   ├── simulate-webhook.js        ← 模拟任意 Webhook 事件
│   ├── reset-db.js                ← 清空 db.json（演示重置用）
│   └── reconcile.js               ← 手动对账脚本
│
└── test-reports/
    ├── latest.json                ← 最新自动化报告（JSON）
    ├── latest.md                  ← 最新自动化报告（Markdown）
    ├── manual-test-todo.json      ← 手动测试待办（auto-test.js 生成）
    ├── final-report-latest.md     ← 最终完整报告（自动化 + 手动合并）
    └── {timestamp}.*              ← 历史报告
```
