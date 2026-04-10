# claude-with

[简体中文](./README_zh.md)

A lightweight wrapper that lets you switch between different environment presets when running [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Configure any environment variables you like — API keys, base URLs, model names, feature flags, etc.

## How It Works

`claude-with` reads model configurations from a JSON file, sets the corresponding environment variables, and launches Claude Code. It also records each session so you can resume them later.

## Usage

```bash
# Start with the default model
claude-with

# Start with a specific model
claude-with glm
claude-with gemini-flash
claude-with gemini-pro
claude-with qwen-coder

# List all available models
claude-with list

# Resume a previous session from history
claude-with history
```

Any additional arguments are passed through to `claude`:

```bash
claude-with gemini-flash --dangerously-skip-permissions
```

## Configuration

Place `claude-with.config.json` in the same directory as the `claude-with` script:

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

- **`default`** — Base environment variables applied to every session. Merged with the selected preset's overrides.
- **Other keys** — Named presets. Each key-value pair is exported as an environment variable. You can set anything — `ANTHROPIC_MODEL`, `ANTHROPIC_BASE_URL`, `ANTHROPIC_API_KEY`, feature flags, or any other env var Claude Code respects.

## Session History

Each session is automatically logged. `claude-with history` presents an interactive menu of recent sessions and resumes the one you select.

History is stored in `claude_history.json` in the same directory as the scripts (last 20 sessions).

## Installation

1. Clone or copy all files (`claude-with`, `claude-history.py`, `claude-with.config.json`) into a directory of your choice
2. Make `claude-with` executable: `chmod +x claude-with`
3. Add the directory to your `PATH`, or alias it: `alias claude-with=/path/to/claude-with`

### Dependencies

- [jq](https://jstedman.github.io/jq/) — JSON parsing
- Python 3 — History management
- `script` — Session recording (built into macOS/Linux)

## License

MIT
