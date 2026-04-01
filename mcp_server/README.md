# backlight-mcp

MCP server for controlling keyboard backlight via Linux sysfs LED nodes.

## Setup

### 1. Find your LED device name

```bash
ls /sys/class/leds/
```

Pick the device you want to control (e.g. `tpacpi::kbd_backlight`).

### 2. Create a `.env` file

Copy the example and set your device name:

```bash
cp .env.example .env
```

Edit `.env`:

```
LED_NAME=tpacpi::kbd_backlight
```

The `.env` file must sit in the `mcp_server/` directory (alongside `pyproject.toml`).

### 3. Install dependencies

```bash
poetry install
```

## Running the server

```bash
poetry run backlight-mcp
```

The server communicates over stdio and is intended to be launched by an MCP client (e.g. Claude Desktop).

## MCP interface

| Type     | Name                  | Description                              |
|----------|-----------------------|------------------------------------------|
| Resource | `leds://brightness`     | Read current brightness (integer)        |
| Resource | `leds://max_brightness` | Read maximum brightness (integer)        |
| Tool     | `set_brightness(value)` | Write brightness as an absolute integer. Out-of-range values are passed through and any kernel error is returned to the client. |
