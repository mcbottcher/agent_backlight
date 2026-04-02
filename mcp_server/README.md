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

### 3. Grant write permission to the brightness node

The `brightness` sysfs node is only writable by root by default. Since the server runs as a regular user, you need to grant write access to it.

One way to do this is with a udev rule that `chmod`s the node whenever the device appears. For example, create `/etc/udev/rules.d/90-backlight.rules`:

```
SUBSYSTEM=="leds", KERNEL=="tpacpi::kbd_backlight", RUN+="/bin/chmod a+w /sys/class/leds/%k/brightness"
```

Replace `tpacpi::kbd_backlight` with your actual device name. Then reload the rules:

```bash
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Note: `max_brightness` is world-readable by default and does not need any permission changes.

### 5. Install dependencies

```bash
poetry install
```

## Running the server

```bash
poetry run backlight-mcp
```

The server communicates over stdio and is intended to be launched by an MCP client (e.g. Claude Desktop).

You can also test the server in isolation by running the server and simply pasting commands into the std in. e.g.

```bash
> {"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"0.1"}}}

> {"jsonrpc":"2.0","method":"notifications/initialized","params":{}}

> {"jsonrpc":"2.0","id":2,"method":"resources/list","params":{}}

> {"jsonrpc":"2.0","id":3,"method":"resources/read","params":{"uri":"leds://brightness"}}

> {"jsonrpc":"2.0","id":4,"method":"resources/read","params":{"uri":"leds://max_brightness"}}
```

It is also possible to run with an MCP development tool, which launches a browser interface to the server.

```bash
poetry run mcp dev src/backlight_mcp/server.py
```

Note: You might need node.js installed, and you need to ensure it is a compatible version. At the time of writing a version over v20 was needed.

Note: By default the MCP viewer uses UV commands to launch the server. Since this project uses poetry, swith the "Command" to `poetry` and the "Arguments" to `run mcp run src/backlight_mcp/server.py`

## MCP interface

| Type     | Name                  | Description                              |
|----------|-----------------------|------------------------------------------|
| Resource | `leds://brightness`     | Read current brightness (integer)        |
| Resource | `leds://max_brightness` | Read maximum brightness (integer)        |
| Tool     | `set_brightness(value)` | Write brightness as an absolute integer. Out-of-range values are passed through and any kernel error is returned to the client. |
