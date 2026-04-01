#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENT_PYTHON="$(cd "$SCRIPT_DIR/mcp_client" && poetry env info --executable)"

exec "$CLIENT_PYTHON" -m backlight_client
