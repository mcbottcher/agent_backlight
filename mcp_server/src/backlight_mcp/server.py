from mcp.server.fastmcp import FastMCP

from backlight_mcp.config import BRIGHTNESS_PATH, MAX_BRIGHTNESS_PATH

mcp = FastMCP("backlight")


@mcp.resource("leds://brightness", mime_type="text/plain")
def get_brightness() -> str:
    """Current brightness value of the configured LED."""
    with open(BRIGHTNESS_PATH) as f:
        return f.read().strip()


@mcp.resource("leds://max_brightness", mime_type="text/plain")
def get_max_brightness() -> str:
    """Maximum brightness value supported by the configured LED."""
    with open(MAX_BRIGHTNESS_PATH) as f:
        return f.read().strip()


@mcp.tool()
def set_brightness(value: int) -> str:
    """Set the brightness of the configured LED to an absolute integer value.

    Writes directly to the sysfs node. Out-of-range values will be rejected
    by the kernel with an error returned to the caller.
    """
    with open(BRIGHTNESS_PATH, "w") as f:
        f.write(str(value))
    return f"Brightness set to {value}"
