# backlight-client

MCP client for reading and controlling keyboard backlight. Connects to `backlight-mcp` over stdio by spawning it as a subprocess.

## Setup

### 1. Install the server first

The client spawns the server as a subprocess, so the server must be installed and configured before running the client. Follow the setup steps in `mcp_server/README.md`.

### 2. Find the server's Python interpreter

The client needs to know which Python executable to use when spawning the server. Get it by running:

```bash
cd ../mcp_server && poetry env info --executable
```

### 3. Create a `.env` file

```bash
cp .env.example .env
```

Edit `.env` and set `SERVER_PYTHON` to the path from the previous step:

```
SERVER_PYTHON=/home/you/.cache/pypoetry/virtualenvs/backlight-mcp-xxxx-py3.10/bin/python
SERVER_MODULE=backlight_mcp
```

### 4. Install dependencies

```bash
poetry install
```

## Running

```bash
poetry run backlight-client
```

Or from the repo root using the launcher script:

```bash
./launch.sh
```

## How it works

The client uses the MCP Python SDK's `stdio_client` to spawn the server as a child process and communicate with it over stdin/stdout. The server process is started on demand and exits when the client session ends.
