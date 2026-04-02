# backlight-client

A Claude-powered chatbot for controlling your keyboard backlight. It connects to `backlight-mcp` over stdio and exposes the backlight tools to Claude, so you can control the LED through natural conversation.

## Setup

### 1. Create a `.env` file

```bash
cp .env.example .env
```

Edit `.env` and set your Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com/)):

```
ANTHROPIC_API_KEY=sk-ant-...
```

### 2. Configure the server

The server is installed as a dependency of this package, but it still needs its own `.env` to know which LED device to control:

```bash
cd ../mcp_server
cp .env.example .env   # set LED_NAME to your device
```

See `mcp_server/README.md` for details on finding your LED device name.

### 3. Install dependencies

```bash
cd ../mcp_client
poetry install
```

This installs both the client and the server package into the same virtualenv.

## Running

```bash
poetry run backlight-client
```

## Usage

Once running, type naturally:

```
You: what's the current brightness?
You: set it to max
You: turn off the backlight
You: quit
```

## How it works

The client spawns the MCP server (`backlight_mcp`) as a child process using `sys.executable`, so both run in the same virtualenv — no separate Python path needed. It registers two resource-reading tools (`get_brightness`, `get_max_brightness`) and wraps the server's `set_brightness` MCP tool, then passes all three to Claude (`claude-sonnet-4-6`) via the Anthropic SDK's tool runner. Claude decides which tools to call based on your message and responds in plain language.
