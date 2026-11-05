# AI Config

一套从日常使用中整理的 Codex 配置：直接表达、简单开发、按任务选择技能。

**v0.1 支持 Windows PowerShell 5.1+。** 适合希望参考全局规则、选择性安装个人技能的人。每位使用者需要自己的 Codex 登录和可用模型。

## 包含什么

| 内容 | 用途 | 安装方式 |
|---|---|---|
| [通用规则](codex/AGENTS.md) | 中文直接表达、简单开发、合理验证 | 安装器的 Rules 模块 |
| [direct-output](skills/direct-output/SKILL.md) | 按场景给出结论和必要细节 | 安装器的 Skills 模块 |
| [report-writing](skills/report-writing/SKILL.md) | 正式报告的结构、论证、证据与修改 | 安装器的 Skills 模块 |
| [基础配置示例](codex/config.example.toml) | 可手动选择的设置 | 自行合并 |
| [MCP 示例](codex/mcp.example.toml) | 本地进程与远程服务的配置结构 | 填写自己的服务后合并 |
| [扩展清单](manifests/extensions.json) | 第三方技能、官方插件与 MCP 的用途和来源 | 按需自行安装 |

本仓库不提供模型账号、API 额度或共享凭据。官方插件和第三方技能通过各自来源安装；安装器不下载这些扩展。

## 开始使用

先安装并登录 Codex，再下载或克隆本仓库到你自己的项目目录：

```powershell
git clone https://github.com/Deng919/ai-config.git
cd ai-config

# 先看即将安装的文件，不写入配置
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -WhatIf

# 安装规则和两个技能
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1
```

`ExecutionPolicy Bypass` 只用于本次脚本进程，不修改系统执行策略。运行前可以阅读 [install.ps1](install.ps1)。

默认写入：

- `%USERPROFILE%\.codex\AGENTS.md`
- `%USERPROFILE%\.agents\skills\direct-output\`
- `%USERPROFILE%\.agents\skills\report-writing\`

已设置 `CODEX_HOME` 时，规则和备份写入该目录；技能仍在用户目录的 `.agents/skills`。也可使用 `-CodexHome` 指定规则目录。用于测试或安装到其他用户目录时，可传入 `-TargetHome`；此时忽略环境中的 `CODEX_HOME`，除非同时显式指定 `-CodexHome`。

只安装一个模块：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Components Skills
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Components Rules
```

安装后新开一个 Codex 聊天，检查技能是否可见，也可直接点名 `$direct-output` 或 `$report-writing`。配置分层与技能位置参考 [OpenAI 官方定制说明](https://developers.openai.com/codex/concepts/customization)。

## 已经有自己的配置

相同文件会跳过。不同文件会先显示行差异并停止，不写入本次选择的其他文件。你可以手动合并，也可明确选择备份后替换：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -ReplaceExisting
```

备份位置为 `<CodexHome>\backups\ai-config\<时间与编号>`。其中 `manifest.json` 记录每个原文件和备份文件的对应关系。替换前会核对备份内容；安装失败时已生成的备份会保留。

恢复时按 `manifest.json` 把备份复制回原路径；首次安装的新文件没有旧版本，可按上面的安装位置手动移除。本脚本不修改 `config.toml`，不修改项目文件，不运行第三方安装命令。目标路径经过目录联接或符号链接时会拒绝安装，改用真实目录路径即可。

## 自行配置

- [本机参数和可选习惯](docs/customization.md)：运行环境、文件目录、自动推送、图片生成。
- [扩展选择](docs/extensions.md)：官方能力、第三方来源和服务依赖。
- [维护与验证](docs/maintenance.md)：更新、测试、发布检查。

## 来源与许可

这两个技能来自维护者提供的本地个人配置，经整理后分享；原始上游来源没有登记，见 [来源记录](manifests/extensions.json)。其他第三方内容仅登记来源，不随仓库复制。仓库内发布的配置、技能、文档和脚本采用 [MIT](LICENSE) 许可；外部项目保留各自许可证。

已移除原环境中的固定盘符、个人路径、账号管理器、历史会话和日志。支持范围为 Windows；macOS/Linux 使用者可以手动参考文本配置，安装脚本未在这些系统验证。
