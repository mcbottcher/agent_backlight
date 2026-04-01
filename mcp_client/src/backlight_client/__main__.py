import asyncio

from backlight_client.client import run


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
