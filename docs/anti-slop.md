# anti-slop 参考与取舍

日期：2026-11-13。

来源：[miqdadbadjuber/anti-slop](https://github.com/miqdadbadjuber/anti-slop)，第三方项目。审阅版本固定为提交 [54e39872aeba6a699b40f6a68f51307c3eea2901](https://github.com/miqdadbadjuber/anti-slop/tree/54e39872aeba6a699b40f6a68f51307c3eea2901)，不表示已跟进其后续更新。

## 已采用的内容

- 附带的 `direct-output` 增加三个本地编写的中文反例：空泛宣传、无来源背书、缺少具体信息的口号。保留用户原本的事实与语气，不按标点或词语鉴定 AI 文本。
- 维护者本机的 `frontend-automation-qa` 补充了受影响流程的真实交互与状态、内容导致的布局断点、中间屏幕宽度、长内容、键盘和焦点、语义、文字对比度及减少动态效果检查。
- 验证范围随改动选择：新页面和布局修改检查桌面与手机，并观察中间宽度；非布局的小改动检查受影响视图，有具体风险再扩展。

本仓库仍只分发 `direct-output` 和 `report-writing` 两个技能。前端 QA 的本机完整技能未随仓库发布，使用者可以把这里的检查思路合并到自己的 QA 流程。

## 使用边界

anti-slop 仅作可选参考，不作为全局依赖。安装器不下载它，不执行其 CLI，不添加入口指令，也不安装上游六个技能。

保留现有 `report-writing` 的论证与引用职责。长文或营销文案先按具体任务手动审阅；出现重复需求后，再考虑独立编辑技能。

未采用的规则包括：固定交付报告格式、对所有小改动穷举全部控件和主题、默认增加明暗主题、按固定行数删注释、绝对禁止某种标点，以及统一规定视觉风格。需求中的品牌、版式、功能和用户文风优先。

## 手动审阅示例

### 长文或营销文案

> 检查这段文字中缺少信息的宣传、没有来源的背书和重复口号，给出具体修改。保留我的事实、语气和有用途的修辞，不补造数据、来源或用户评价。遇到依据缺失时直接标明；不要按固定词表机械替换。

### 页面检查

> 检查这次改动影响的页面和主要操作：按钮与链接是否有效，相关加载、空数据和错误状态是否清楚；布局修改检查桌面、手机和容易断裂的中间宽度；控件修改检查键盘操作、焦点和名称，颜色修改测量文字对比度。按实际风险选检查项，给出具体问题与已验证范围。

这些是任务提示示例，不会创建新的自动触发技能，也不要求加载 anti-slop 核心流程。

## 标准修正

上游审阅版本的部分条目把大号文字门槛写成 `18px+`。本地新增规则依据 [W3C WCAG 2.2：Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)：普通文字至少 4.5:1，大号文字至少 3:1，具体例外以原文为准。

对于拉丁文字，大号指至少 18 pt 常规字重（24 CSS px），或 14 pt 粗体（18 又 2/3 CSS px）；中日韩字体需考虑等效字号。普通 18 CSS px 文字不自动属于大号。测量结果不能向上取整以判为通过，抽样检查也不等于完整无障碍合规评估。

## 来源与维护

新增中文示例和前端指引为本地编写，选题与检查思路参考了上游的 [copywriting](https://github.com/miqdadbadjuber/anti-slop/blob/54e39872aeba6a699b40f6a68f51307c3eea2901/skills/antislop-copywriting/SKILL.md)、[UI](https://github.com/miqdadbadjuber/anti-slop/blob/54e39872aeba6a699b40f6a68f51307c3eea2901/skills/antislop-ui/SKILL.md)、[human](https://github.com/miqdadbadjuber/anti-slop/blob/54e39872aeba6a699b40f6a68f51307c3eea2901/skills/antislop-human/SKILL.md) 和 [layoutmobile](https://github.com/miqdadbadjuber/anti-slop/blob/54e39872aeba6a699b40f6a68f51307c3eea2901/skills/antislop-layoutmobile/SKILL.md) 模块。上游采用 MIT，版权归 Miqdad Badjuber，许可全文保留在 [anti-slop-MIT.txt](licenses/anti-slop-MIT.txt)。

后续实质性改编上游技能时，应使用能区分本地版本的名称，登记基准提交、修改范围并保留许可；不要把本地改编标成官方能力或未经修改的上游版本。

当前选择依据源码审阅，尚未进行输出效果对照。评估时可用同一任务比较现有规则与新增规则，观察事实保真、发现的具体问题，以及额外询问和报告负担，再根据实际结果调整。
