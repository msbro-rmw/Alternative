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

flask_app = Flask(__name__)

@flask_app.route("/")
def health():
    return {"status": "ok"}, 200

@flask_app.route("/health")
def healthcheck():
    return {"status": "healthy"}, 200

def run_flask():
    from werkzeug.serving import make_server
    port = int(os.environ.get("PORT", 8080))
    server = make_server("0.0.0.0", port, flask_app)
    server.serve_forever()

async def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("✅ Flask started")

    logger.info("⏳ Starting userbot...")
    await userbot.start()
    logger.info("✅ Userbot started")

    logger.info("⏳ Starting bot...")
    await bot.start()
    logger.info("✅ Bot started")
    logger.info("🚀 Running!")

    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
