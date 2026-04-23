"""
Run this script ONCE locally to generate your Pyrogram session string.
Then set SESSION_STRING as an environment variable on Render.

Usage:
    python utils/gen_session.py
"""

import asyncio
from pyrogram import Client

API_ID   = 38498066          # <-- Same as in bot/main.py
API_HASH = "c9696114751feacdeb1b4487f5839a1a"  # <-- Same as in bot/main.py


async def generate():
    async with Client(
        "session_generator",
        api_id=API_ID,
        api_hash=API_HASH,
    ) as app:
        session_string = await app.export_session_string()
        print("\n" + "=" * 60)
        print("YOUR SESSION STRING (save this as SESSION_STRING env var):")
        print("=" * 60)
        print(session_string)
        print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(generate())
