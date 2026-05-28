# OpenBusiness

> **AI 驱动、证据优先的商业模式逆向工程工具。** 输入一家公司的名字，自动产出一份带「事实 / 推断 / 缺口」分层标注的商业模式画布报告。

灵感来自 [TradingAgents](https://github.com/TauricResearch/TradingAgents)，但**故意没有照搬**它的牛熊辩论结构 — 商业分析的产出不是 buy/sell 投票，而是结构化解构。

---

## 🎯 它能做什么

```
$ openbusiness analyze "Notion" --domain notion.so

  🔍 Evidence Collector         (Tavily + Firecrawl + SEC EDGAR 抓证据)
  👥 JTBD Analyst               (谁付钱 / 谁使用 / 完成什么任务)
  💎 Value Prop Analyst         (10x Better 测试)
  🚀 GTM Analyst                (PLG / Sales-led / Marketplace / Community ...)
  💰 Unit Economics Analyst     (LTV / CAC / 盈亏平衡, 纯数学计算)
  🛡️ Moat Analyst               (5 类壁垒 + 波特五力 + Counter-position)
  🧱 Business Model Synthesizer (生成画布)
  🔬 Assumption Stress Tester   (找出哪个假设错了画布会塌)
  📝 Finalizer                  (拼成最终报告)

✅ 报告已生成: output/notion_business_model.md
```

报告的每一条结论都打标签：
- 🟢 `[VERIFIED:url]` — 有源可查
- 🟡 `[INFERRED]` — LLM 基于上下文推断
- 🔴 `[MISSING]` — 缺数据，影响信心

---

## 🛠️ 5 分钟安装教程

### Step 1 · 克隆仓库

```bash
git clone https://github.com/wanikua/OpenBusiness.git
cd OpenBusiness
```

### Step 2 · 跑安装脚本

```bash
./install.sh
```

这个脚本会做 4 件事，全程交互式提示：

1. **检查 Python** — 需要 3.10+。没有它会告诉你去哪下载。
2. **建虚拟环境** — 在 `.venv/`，问你 Y/n。建议同意，避免污染系统 Python。
3. **装依赖** — `pip install -e .`，把所有需要的库装好。
4. **跑配置向导** — 提示你输 API key。看下面。

### Step 3 · 配置向导问什么

向导会顺序问你这几个问题：

| 问题 | 怎么答 |
|------|--------|
| `选择 LLM 提供方 [openai/anthropic]` | 二选一。OpenAI 默认。 |
| `OpenAI API Key (sk-...):` 或 `Anthropic API Key (sk-ant-...):` | **必填**。去 [platform.openai.com/api-keys](https://platform.openai.com/api-keys) 或 [console.anthropic.com](https://console.anthropic.com/) 拿。输入时不会回显。 |
| `Tavily API Key (Web 搜索, 可选):` | **可选**。直接回车跳过。如果想要更靠谱的事实采集，去 [tavily.com](https://tavily.com) 注册（免费额度够用）。 |
| `Firecrawl API Key (页面抓取, 可选):` | **可选**。直接回车跳过。需要抓官网/定价页时用，去 [firecrawl.dev](https://firecrawl.dev) 注册。 |

> **不填 Tavily / Firecrawl 会怎样？** 流水线照跑，只是分析里 `[INFERRED]` 占比会更高 — 因为没法抓真实证据，只能靠 LLM 已有知识。不影响功能，影响可信度。

配置保存到 `~/.config/openbusiness/config.toml`，权限 `0600` (只有你能读)。

### Step 4 · 跑第一次分析

```bash
# 如果用了 venv，先激活
source .venv/bin/activate

# 拆一家公司
openbusiness analyze "Notion" --domain notion.so
```

报告输出到 `output/notion_business_model.md`。

---

## 📚 命令行用法

```bash
openbusiness config              # 首次配置向导 (或显示当前配置)
openbusiness config --reset      # 强制重新输入所有 key
openbusiness show                # 查看当前配置 (不显示完整 key)

openbusiness analyze "Notion" --domain notion.so
openbusiness analyze "Costco"   --ticker COST
openbusiness analyze "Vercel"   --domain vercel.com --output reports/
```

参数：
- `--domain / -d` : 官网域名，给 evidence collector 抓页面用
- `--ticker / -t` : 美股代码 (有的话)，触发 SEC EDGAR 真财报
- `--output / -o` : 报告目录，默认 `output/`

---

## 🌍 环境变量覆盖

环境变量始终优先于配置文件 — 适合 CI、容器、临时切换 key：

```bash
export OPENBUSINESS_PROVIDER=anthropic
export ANTHROPIC_API_KEY=sk-ant-xxx
export TAVILY_API_KEY=tvly-xxx
export FIRECRAWL_API_KEY=fc-xxx

openbusiness analyze "Notion" --domain notion.so
```

---

## 🏗️ 架构

```
User
  │  (company name + domain + ticker)
  ▼
┌─────────────────────────────────────┐
│  Evidence Collector                  │ ← Tavily 搜索 + Firecrawl 抓页面
│                                      │   + SEC EDGAR 真财报
└────────┬─────────────────────────────┘
         │  evidence_pack (Markdown 证据包)
         ▼
┌─────────────────────────────────────┐
│  JTBD Analyst                        │ ← 谁付钱、谁使用、什么任务
└────────┬─────────────────────────────┘
         │  + jtbd_report
         ▼
┌─────────────────────────────────────┐
│  Value Prop Analyst                  │ ← 10x Better 测试
└────────┬─────────────────────────────┘
         │  + value_prop_report
         ▼
┌─────────────────────────────────────┐
│  GTM Analyst                         │ ← 真实分销渠道枚举
└────────┬─────────────────────────────┘
         │  + gtm_report
         ▼
┌─────────────────────────────────────┐
│  Unit Economics Analyst              │ ← LTV/CAC 工具 (纯数学)
└────────┬─────────────────────────────┘
         │  + unit_econ_report
         ▼
┌─────────────────────────────────────┐
│  Moat & Competition Analyst          │ ← 5 类壁垒 + 波特五力
└────────┬─────────────────────────────┘
         │  + moat_report
         ▼
┌─────────────────────────────────────┐
│  Business Model Synthesizer          │ ← 合成画布 (保留所有标签)
└────────┬─────────────────────────────┘
         │  + canvas_report
         ▼
┌─────────────────────────────────────┐
│  Assumption Stress Tester            │ ← 找出致命假设和缺口
└────────┬─────────────────────────────┘
         │  + stress_test_report
         ▼
┌─────────────────────────────────────┐
│  Finalizer                           │ ← 整合输出
└────────┬─────────────────────────────┘
         ▼
 output/<company>_business_model.md
```

**核心设计原则**：
- **Linear flow, no debate.** 商业分析的产出是分解，不是投票。
- **Evidence first.** 任何 LLM 分析前先抓真实证据。
- **Tag every claim.** 每条结论标 VERIFIED / INFERRED / MISSING。
- **Tools are pure math.** 单体经济计算是 Python 函数，不靠 LLM 算账。
- **Two LLM tiers.** Analyst 用 mini/haiku，Synthesizer 用 deep model，省钱。

---

## 📂 项目结构

```
OpenBusiness/
├── install.sh                       # 一键安装脚本 (你刚跑过的)
├── pyproject.toml                   # Python 包定义
├── README.md
├── .env.example                     # 环境变量示例
├── openbusiness/
│   ├── cli.py                       # CLI 入口 (config / show / analyze)
│   ├── agents/
│   │   ├── analysts/
│   │   │   ├── evidence_collector.py
│   │   │   ├── jtbd_analyst.py
│   │   │   ├── value_prop_analyst.py
│   │   │   ├── gtm_analyst.py
│   │   │   ├── unit_econ_analyst.py
│   │   │   ├── moat_analyst.py
│   │   │   ├── synthesizer.py
│   │   │   ├── stress_tester.py
│   │   │   └── finalizer.py
│   │   └── utils/agent_state.py     # 共享 TypedDict 状态
│   ├── tools/
│   │   ├── evidence_tools.py        # Tavily / Firecrawl / SEC EDGAR
│   │   └── financial_tools.py       # LTV/CAC 计算器 (纯函数)
│   ├── graph/setup.py               # LangGraph 线性流水线
│   └── llm_clients/
│       ├── config.py                # 配置文件 + 环境变量解析
│       └── factory.py               # OpenAI / Anthropic 双层工厂
└── output/                          # 报告输出目录 (.gitignored)
```

---

## 📤 输出报告示例

```markdown
# 📊 OpenBusiness 商业模式逆向工程报告

**Target:** Notion | **Confidence:** Plausible

## 1. Business Model Canvas
| 核心伙伴 (KP) | 关键业务 (KA) | 价值主张 (VP) | 客户关系 (CR) | 客户细分 (CS) |
| ... | ... | All-in-one workspace [VERIFIED:notion.so] | PLG self-serve [INFERRED] | ... |
| | 核心资源: AI Q&A, templates [VERIFIED:...] | | 渠道: PLG + community [VERIFIED:...] | |
| 成本: 研发 + infra [INFERRED] | 收入: Free / Plus $10/seat / Business $20 [VERIFIED:notion.so/pricing] |

## 2. Key Facts Layered
### 🟢 Verified Facts
- 定价: Free / Plus $10/seat/mo / Business $20 / Enterprise [VERIFIED:notion.so/pricing]
- ...

### 🟡 Inferred Assumptions
- Churn ~3-5%/月 (基于 PLG SaaS 行业基准) [INFERRED]
- ...

### 🔴 Missing Data
- 实际 CAC 与 LTV [MISSING]
- ...

## 3. Stress Test
- High-priority assumption: 若 Churn 实为 8%+，LTV 折半，整个画布塌
- Fatal data gap: 没有真实留存数据
- One-line verdict: Plausible

## 4. Next Steps
- 想继续深挖: 找 Notion 公开的留存/付费转化数据
- 想抄商业模式: 抄它的模板/社区飞轮
- 想攻击: 攻它的 "all-in-one" 反面 — 做垂直深耕的单点工具
```

---

## 🔍 排错

**`./install.sh: Permission denied`**
→ `chmod +x install.sh && ./install.sh`

**`python: command not found`**
→ macOS: `brew install python@3.12`
→ Linux: `apt install python3.12 python3.12-venv` 或类似
→ Windows: 从 https://www.python.org/downloads/ 装

**`openbusiness: command not found`**
→ 如果用了 venv，每次开新终端要先 `source .venv/bin/activate`

**`OPENAI_API_KEY ... is invalid`**
→ Key 不对或没额度。`openbusiness config --reset` 重输

**报告全是 [INFERRED]**
→ 你没配 Tavily/Firecrawl。`openbusiness config --reset` 补上 key

**LangGraph 报错 `Could not stream from node`**
→ 通常是 LLM 端的限速。等 1 分钟重试，或换 deep model 到更便宜的型号

---

## 🤝 贡献 / 扩展

加一个新分析师：

1. 在 `openbusiness/agents/analysts/` 写 `your_analyst.py`，导出 `create_your_analyst(llm)`
2. 在 `openbusiness/agents/analysts/__init__.py` 加导出
3. 在 `openbusiness/graph/setup.py` 把节点插进流水线

加一个新工具：

1. 在 `openbusiness/tools/` 加 `@tool` 装饰的函数
2. 在某个 analyst 里 `bind_tools([your_tool])`
3. **返回数据必须带 `[VERIFIED:source]` 或在 key 缺失时返回 `warning` 字段**

---

## 📄 License

MIT
