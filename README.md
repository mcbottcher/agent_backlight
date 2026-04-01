# agent_backlight
The new agent joining MI6. Agent Backlight will be responsible for controlling the keyboard backlight on your PC.

His mission is to help me learn how to use an MCP server and client, and how to integrate these with a LLM tool like Claude.

## Repository structure

```
agent_backlight/
├── mcp_server/   # MCP server — exposes backlight control over stdio
├── mcp_client/   # MCP client — connects to the server and reads/sets brightness
└── launch.sh     # Launcher — runs the client (which spawns the server internally)
```

## Quickstart

### 1. Set up the server

```bash
cd mcp_server
cp .env.example .env       # set LED_NAME to your device
poetry install
```

See `mcp_server/README.md` for details on finding your LED device name.

### 2. Set up the client

```bash
cd mcp_client
cp .env.example .env       # set SERVER_PYTHON to the server's virtualenv Python
poetry install
```

See `mcp_client/README.md` for details on finding the right Python path.

### 3. Run

From the repo root:

```bash
./launch.sh
```

This launches the client, which spawns the server as a subprocess and communicates with it over stdio.
