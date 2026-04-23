import asyncio
import os
import logging
import threading
from flask import Flask
from bot.main import bot, userbot

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ─── Flask (health check only) ─────────────────────────────────────────────────
flask_app = Flask(__name__)

@flask_app.route("/")
def health():
    return {"status": "ok"}, 200

@flask_app.route("/health")
def healthcheck():
    return {"status": "healthy"}, 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    # Use werkzeug directly to avoid debug/reloader issues
    from werkzeug.serving import make_server
    server = make_server("0.0.0.0", port, flask_app)
    logger.info(f"Flask running on port {port}")
    server.serve_forever()

# ─── Main async entry ──────────────────────────────────────────────────────────
async def main():
    # Flask in background thread FIRST
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # Start userbot
    await userbot.start()
    logger.info("✅ Userbot started")

    # Start bot
    await bot.start()
    logger.info("✅ Bot started")

    logger.info("🚀 Running! Press Ctrl+C to stop.")

    # Keep alive — simple loop instead of pyrogram idle
    try:
        while True:
            await asyncio.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        await bot.stop()
        await userbot.stop()
        logger.info("Stopped.")

if __name__ == "__main__":
    asyncio.run(main())
