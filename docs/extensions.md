# 按需选择扩展

完整来源记录见 [extensions.json](../manifests/extensions.json)。清单表示整理时维护者的配置参考，不表示使用本仓库就会安装或启用这些能力。

## 官方能力

- Word：documents。
- PDF：pdf。
- 演示：presentations。
- 表格：spreadsheets。
- 可复用模板：template-creator。
- 聊天内可视化：visualize。
- 界面与浏览器操作：computer-use，以及运行环境提供的相关工具插件。
- 技能维护：Codex 随附的 skill-creator、skill-installer。

通过使用者的 Codex 插件入口查看可用项、权限和安装说明。账号、客户端版本和平台不同，可用能力也可能不同；不复制客户端插件缓存。

## 第三方技能

| 来源 | 本机使用过的能力 |
|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 需求讨论、规划、测试、调试、评审和 Git 工作流 |
| [anysearch-ai/anysearch-skill](https://github.com/anysearch-ai/anysearch-skill) | 搜索和正文提取 |
| [openai/skills](https://github.com/openai/skills) | playwright 技能；来源为 OpenAI 仓库，个人安装 |
| [beita6969/scienceclaw](https://github.com/beita6969/scienceclaw) | scientific-reasoning |
| [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) | sympy |
| [quantskills/skill-pandaai-factor-online](https://github.com/quantskills/skill-pandaai-factor-online) | PandaAI 因子分析 |

这些地址来自历史安装登记，本次未逐一验证上游最新版本。查看其当前说明、许可证和依赖后再选择安装，不默认整套装入。

## MCP 服务

| 名称 | 用途 | 本仓库提供什么 |
|---|---|---|
| anysearch | 外部搜索 | 用途登记；按服务方说明配置 |
| chatgpt_bridge | 本地图片/聊天桥接 | [项目来源](https://github.com/Deng919/gpttoimage)，独立配置账号 |
| pandadata | 数据平台接口 | 用途登记；使用者自行取得服务地址和授权 |
| rea | 本地程序逆向分析 | 用途登记；需要独立安装 REA 及相应后端 |
| node_repl | 客户端提供的 JS/浏览器工具运行环境 | 由客户端管理，不从维护者电脑复制启动路径和进程参数 |

[mcp.example.toml](../codex/mcp.example.toml) 是禁用的结构示例，域名和脚本路径是占位值。它不会直接连接上述服务。
