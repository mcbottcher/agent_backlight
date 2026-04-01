import asyncio

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from backlight_client.config import SERVER_MODULE, SERVER_PYTHON


async def run() -> None:
    server_params = StdioServerParameters(
        command=SERVER_PYTHON,
        args=["-m", SERVER_MODULE],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  {tool.name}: {tool.description}")

            resources = await session.list_resources()
            print("\nAvailable resources:")
            for resource in resources.resources:
                print(f"  {resource.uri}: {resource.description}")

            brightness = await session.read_resource("leds://brightness")
            print(f"\nCurrent brightness: {brightness.contents[0].text}")

            max_brightness = await session.read_resource("leds://max_brightness")
            print(f"Max brightness: {max_brightness.contents[0].text}")

            level = 0
            while True:
                print(f"Setting brightness to {level}")
                await session.call_tool("set_brightness", {"value": level})
                level = (level + 1) % 3
                await asyncio.sleep(1)
