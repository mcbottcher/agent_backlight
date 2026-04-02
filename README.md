# agent_backlight
The new agent joining MI6. Agent Backlight will be responsible for controlling the keyboard backlight on your PC.

His mission is to help me learn how to use an MCP server and client, and how to integrate these with a LLM tool like Claude.

## Repository structure

```
agent_backlight/
├── mcp_server/   # MCP server — exposes backlight control over stdio
└── mcp_client/   # Chatbot — talks to Claude, which controls the backlight via MCP
```

## Quickstart

### 1. Configure the server

```bash
cd mcp_server
cp .env.example .env       # set LED_NAME to your device
```

See `mcp_server/README.md` for details on finding your LED device name and configuring permissions.

### 2. Set up the client

```bash
cd ../mcp_client
cp .env.example .env       # set ANTHROPIC_API_KEY
poetry install             # also installs the server package
```

### 3. Run

```bash
poetry run backlight-client
```

The chatbot spawns the MCP server as a subprocess and connects Claude to it. You can then chat naturally — ask about the current brightness, set it, turn it off, etc.
