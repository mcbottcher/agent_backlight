import asyncio

from anthropic import AsyncAnthropic, beta_async_tool
from anthropic.lib.tools.mcp import async_mcp_tool
from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from backlight_client.config import SERVER_MODULE, SERVER_PYTHON


SYSTEM_PROMPT = """You are a keyboard backlight assistant. You help the user control and \
monitor their keyboard LED backlight. You have tools to read the current brightness, read \
the maximum brightness, and set the brightness to an integer value. Be concise."""


async def run() -> None:
    server_params = StdioServerParameters(
        command=SERVER_PYTHON,
        args=["-m", SERVER_MODULE],
    )

    client = AsyncAnthropic()

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            mcp_tools = [async_mcp_tool(t, session) for t in tools_result.tools]

            @beta_async_tool
            async def get_brightness() -> str:
                """Get the current brightness value of the keyboard LED."""
                result = await session.read_resource("leds://brightness")
                return result.contents[0].text

            @beta_async_tool
            async def get_max_brightness() -> str:
                """Get the maximum brightness value supported by the keyboard LED."""
                result = await session.read_resource("leds://max_brightness")
                return result.contents[0].text

            all_tools = [get_brightness, get_max_brightness] + mcp_tools

            messages = []
            print("Keyboard Backlight Chatbot — type 'quit' to exit")
            print("-" * 50)

            while True:
                try:
                    user_input = input("\nYou: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nGoodbye!")
                    break

                if user_input.lower() in ("quit", "exit"):
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                messages.append({"role": "user", "content": user_input})

                response_text = ""
                runner = client.beta.messages.tool_runner(
                    model="claude-sonnet-4-6",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    tools=all_tools,
                    messages=messages,
                )

                async for message in runner:
                    for block in message.content:
                        if hasattr(block, "text"):
                            response_text = block.text

                print(f"\nAssistant: {response_text}")
                messages.append({"role": "assistant", "content": response_text})
