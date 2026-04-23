import asyncio
import threading
import logging
import os

from flask import Flask
from pyrogram import idle

from bot.main import bot, userbot

logger = logging.getLogger(__name__)

# ─── Flask (for Render health-check / keep-alive) ──────────────────────────────
flask_app = Flask(__name__)

@flask_app.route("/")
def health():
    return {"status": "ok", "service": "Alternative Extractor Bot"}, 200

@flask_app.route("/health")
def healthcheck():
    return {"status": "healthy"}, 200


def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)


async def main():
    # Start both clients
    await userbot.start()
    logger.info("✅ Userbot started")

    await bot.start()
    logger.info("✅ Bot started")

    # Run Flask in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info(f"✅ Flask server running on port {os.environ.get('PORT', 8080)}")

    logger.info("🚀 Alternative Extractor Bot is running!")
    await idle()

    # Cleanup
    await bot.stop()
    await userbot.stop()


if __name__ == "__main__":
    asyncio.run(main())
