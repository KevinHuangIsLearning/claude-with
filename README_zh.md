# claude-with

[English](./README.md)

一个轻量级的封装库，让您在运行 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 时，可以在不同的环境预设之间切换。您可以配置任何所需的环境变量，例如 API 密钥、基本 URL、模型名称、功能标志等等。

## 工作原理

`claude-with` 从 JSON 文件读取模型配置，设置相应的环境变量，并启动 Claude Code。它还会记录每次会话，以便您稍后恢复。

## 用法

```bash
# 使用默认模型启动
claude-with

# 使用特定模型启动
claude-with glm
claude-with gemini-flash
claude-with gemini-pro
claude-with qwen-coder

# 列出所有可用模型
claude-with list

# 从历史记录恢复之前的会话
claude-with history
```

任何其他参数都会传递给 `claude`：

```bash
claude-with gemini-flash --dangerously-skip-permissions
```

## 配置

将 `claude-with.config.json` 放在与 `claude-with` 脚本相同的目录中：

```json
{
    "default": {
        "OPENROUTER_API_KEY": "sk-or-v1-...",
        "ANTHROPIC_BASE_URL": "https://openrouter.ai/api",
        "ANTHROPIC_AUTH_TOKEN": "$OPENROUTER_API_KEY",
        "ANTHROPIC_API_KEY": "",
        "CLAUDE_CODE_NO_FLICKER": "1"
    },
    "glm": {
        "ANTHROPIC_MODEL": "z-ai/glm-5.1"
    },
    "gemini-pro": {
        "ANTHROPIC_MODEL": "google/gemini-3.1-pro-preview"
    },
    "gemini-flash": {
        "ANTHROPIC_MODEL": "google/gemini-3-flash-preview"
    },
    "qwen-coder": {
        "ANTHROPIC_MODEL": "qwen/qwen3-coder"
    }
}
```

- **`default`** — 应用于每个会话的基本环境变量。与所选预设的覆盖值合并。

- **其他键** — 命名预设。每个键值对都会导出为环境变量。您可以设置任何内容，例如 `ANTHROPIC_MODEL`、`ANTHROPIC_BASE_URL`、`ANTHROPIC_API_KEY`、功能标志或 Claude Code 支持的任何其他环境变量。

## 会话历史记录

每个会话都会自动记录。`claude-with history` 会显示一个最近会话的交互式菜单，并恢复您选择的会话。

历史记录存储在与脚本位于同一目录下的 `claude_history.json` 文件中（最近 20 个会话）。

## 安装

1. 将所有文件（`claude-with`、`claude-history.py`、`claude-with.config.json`）克隆或复制到您选择的目录。

2. 使 `claude-with` 可执行：`chmod +x claude-with`

3. 安装依赖项

4. 将该目录添加到您的 `PATH` 路径，或为其设置别名：`alias claude-with=/path/to/claude-with`

### 依赖项

- [jq](https://jqlang.org/) — JSON 解析

- Python 3 — 历史记录管理

- `script` — 会话录制（macOS/Linux 内置）

## 许可证

MIT
