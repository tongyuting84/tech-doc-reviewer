---
name: tech-doc-reviewer
description: 企业级中文技术文档撰写与评审 Skill，支持安全合规、事实与任务闭环、参数“大白话”治理、结构与语言、代码命令、网页边界、防误判、链接核验、文档库生命周期与维护性评审、动态分级报告和质检追踪。适用于技术文档创作、改写、发布前评审、网页预览评审、文档库治理及合规检查。
author: tongyuting
metadata:
  version: "2026-10-23.1"
  version_notes: "新增明显人工构造假值豁免：假密码和假资源 ID（如 password@123、Admin@123、subnet-demo123）不作为敏感数据问题，并补充字典词、简单序列、示例语境和低随机度判断标准。"
---

# 技术文档评审专家

对中文技术文档进行可追溯、低误报的撰写与评审。所有技术文档任务使用本 Skill；不得改用 `vsop-doc-review-assistant`。

## 可直接执行的总流程

1. **确认材料**：记录标题、URL、载体、读者、文档类型、使用人；区分源文本、网页抽取、截图和渲染结果。
2. **确定尺度**：区分单篇、跨文档和文档库评审。网页只评创作者可控正文；抽取异常先排除假阳性。无法访问产品或目标链接时标记“待人工核验”，不猜测。
3. **按需加载**：先读来源和严重性，再按下表加载规则；需要解释写作方向时读原则，需要产出/重构时选方法。不要一次读取全部 references。
4. **逐层检查**：先安全、隐私、侵权和严重生产风险，再查事实、任务闭环、参数和一致性，最后查语言、结构和格式；库级材料再查阅读路径、重复与新鲜度。
5. **证据分级**：每条问题锚定原文和具体规则 ID，按实际影响定 P0/P1/P2；“强制”不自动等于 P0。
6. **提出修改**：可重排现有信息、补齐任务必需项和消除歧义；不得无依据新增产品能力、参数、业务结论或步骤。
7. **输出报告**：使用汉堡包五段式，包含 🚨、🔍、✅、🎉；无问题也明确结论。
8. **写入质检记录**：正式评审发现问题后，一条问题一行；无问题不写。失败必须明示。

详细顺序和证据要求见 [评审流程](references/review-workflow.md)。

## 渐进加载路由

| 任务/信号 | 必读 | 条件增量 |
|---|---|---|
| 任意评审或改写 | [来源与规则解释](references/rule-provenance.md)、[严重性与合规](references/severity-and-compliance.md) | 再按下列场景增加 |
| 事实、前提、步骤、验证、失败、回滚、参数 | [内容、参数与操作规则](references/rules/content-and-operations.md) | 写作/重构再读 [任务与参数方法](references/methods/task-and-parameter-writing.md) |
| 文风、通顺度、大白话、循环解释、语病 | [语言与大白话规则](references/rules/language-and-style.md) | 参数问题同时读内容规则 |
| 标题、段落、列表、表格、图片、链接、标点、空格 | [结构、介质、链接与标点规则](references/rules/structure-format-and-links.md) | 图片视觉项按可见证据处理 |
| 术语、缩略语、数字、单位、示例值 | [术语、数值与示例规则](references/rules/terminology-values-and-examples.md) | — |
| 代码、命令、路径、UI、键盘、警示 | [技术元素规则](references/rules/technical-elements.md) | 高风险操作同时读内容规则 |
| 功能介绍、场景分析、价值表达 | [写作与质量原则](references/principles/writing-and-quality.md) | 按需选 [SCQA/5W1H1E/FFBV](references/methods/scenario-and-value.md) |
| 文档库、跨文档变更、阅读路径、重复、新鲜度 | [文档库治理规则](references/rules/library-governance.md)、[文档库质量原则](references/principles/library-quality.md) | 规划/重构再读 [文档库规划方法](references/methods/library-planning.md) |
| 网页预览或网页抓取 | [网页边界](references/web-content-boundaries.md)、[防误判](references/false-positive-prevention.md) | — |
| 输出评审结论 | [报告格式](references/report-format.md) | — |
| 正式评审且发现问题 | [质检写入](references/quality-record-workflow.md) | 使用 `managing-lark-bitable-data` skill 和 [write_quality_records.py](scripts/write_quality_records.py) |
| 维护规则或追溯来源 | [来源与规则解释](references/rule-provenance.md) | 按稳定规则 ID 定位 `rules/`、`principles/`、`methods/` 中的权威内容 |
| 查询版本历史 | [CHANGELOG](references/CHANGELOG.md) | — |

## 全局判定护栏

- **证据优先**：只报告能在原文、可见渲染、可访问目标或可信资料中定位的问题；不足则待核验。
- **三层分工**：`rules/` 是可判定规范；`principles/` 解释目的和信号，不直接充当硬规则；`methods/` 是可选方法，不机械套模板。
- **来源与效力分离**：W/W2 是基础规范，W3 是大白话专项，W4 是结构化写作，W5 是文档库质量，B 是后续实践，E 是防误判护栏；详情以来源索引为准。
- **动态等级**：安全、隐私、侵权、真实云资源 ID 和严重生产风险为 P0；普通文风格式通常 P1/P2；事实、步骤、参数和代码按用户影响动态调整。
- **结构优化允许**：可重排、拆分、补齐任务必需项；新增事实须有依据。TL;DR、固定模板、每篇生命周期五阶段只能按场景建议。
- **介质不机械排序**：图、表、列表、文字按认知收益、可访问性和维护成本选择；“图 > 表 > 文字”不是硬规则。
- **量化门槛可配置**：开头 3 行、FAQ Top 5、7 天闭环仅在团队已配置适用范围和口径时作为门禁。
- **视觉条件化**：字体、像素、边框、分页、行首禁则、截图清晰度等，纯文本不可判断时转人工核验。
- **网页边界**：忽略不可控导航、Footer、自动元数据和 TDK；正文 H1 仍在范围。
- **抽取防误判**：异常断行、空格、表格粘连、代码/UI 标签切分先还原上下文。
- **链接三重检查**：分开检查可达性、目标一致性、锚点准确性；权限或网络受限时分别标未核验。
- **真实资源信息**：真实可用云资源 ID、密钥、账号、公网 IP 等暴露按 P0；明确占位符、RFC 5737 文档保留段与 RFC 1918 私网段示例不报。
- **Markdown 边界**：不机械评审源码风格；导致渲染、链接、代码含义或内容错误时按影响报告。
- **UI 措辞**：按钮名后写“按钮”不单独报错；动作与控件不匹配才报告。

## 冲突决策

1. 法律、安全、隐私和真实生产风险优先。
2. 当前产品事实与平台约束优先于旧规范。
3. B 在对应业务场景优先于 W/W2；W3/W4/W5 按具体场景补充，不自动覆盖更具体规则；E 只限制证据与误报。
4. “强制/建议”是规范效力，P0/P1/P2 是本次影响，不得混用。
5. 无法裁决时保留原文，列入待人工核验并说明缺少证据。

## 版本与升级

- 当前版本以 frontmatter `metadata.version` 为准，历史变更以 [CHANGELOG](references/CHANGELOG.md) 为准。
- 当用户提出“检查更新”“升级 Skill”或“拉取最新规范”时，必须读取并完整执行 [Skill 升级流程](references/skill-update-workflow.md)。
- 该 reference 是升级流程的唯一权威来源；未经用户明确要求，不上传、不发布 Skill。
