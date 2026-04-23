import asyncio
import logging
import os
import re
from collections import deque
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ─── Config ────────────────────────────────────────────────────────────────────
API_ID   = 38498066               # <-- Apna API ID yahan dalo
API_HASH = "c9696114751feacdeb1b4487f5839a1a" # <-- Apna API HASH yahan dalo
BOT_TOKEN = os.environ.get("BOT_TOKEN")

UPLOAD_PILOT_BOT = "UploadPilotbot"

# ─── Pyrogram Clients ──────────────────────────────────────────────────────────
bot = Client(
    "alternative_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

userbot = Client(
    "userbot_session",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=os.environ.get("SESSION_STRING"),
)

# ─── Queue ─────────────────────────────────────────────────────────────────────
task_queue: deque = deque()
processing = False


def extract_first_file_id(message: Message) -> str | None:
    """
    Inline keyboard ke SIRF PEHLE button ka file_id extract karo.
    720p ho ya na ho — pehla button jo bhi ho wahi lena hai.
    """
    if not message.reply_markup:
        return None

    pattern = re.compile(
        r"https?://t\.me/UploadPilotbot\?start=(file_[A-Za-z0-9_-]+)",
        re.IGNORECASE,
    )

    for row in message.reply_markup.inline_keyboard:
        for button in row:
            if button.url:
                m = pattern.search(button.url)
                if m:
                    logger.info(f"First button URL found: {button.url}")
                    return m.group(1)  # Sirf pehla milte hi return

    return None


async def fetch_file_from_uploadpilot(file_start_param: str) -> Message | None:
    """Userbot se UploadPilotBot ko /start bhejo aur response capture karo."""
    try:
        await userbot.send_message(UPLOAD_PILOT_BOT, f"/start {file_start_param}")
        logger.info(f"Sent /start {file_start_param} to UploadPilotBot")

        await asyncio.sleep(3)  # 3s kaafi fast hai

        async for msg in userbot.get_chat_history(UPLOAD_PILOT_BOT, limit=1):
            if msg.from_user and msg.from_user.username and \
               msg.from_user.username.lower() == UPLOAD_PILOT_BOT.lower():
                return msg

        return None

    except FloodWait as e:
        logger.warning(f"FloodWait: sleeping {e.value}s")
        await asyncio.sleep(e.value)
        return None
    except Exception as ex:
        logger.error(f"Error fetching from UploadPilotBot: {ex}")
        return None


async def process_queue():
    """Queue se ek ek task process karo."""
    global processing
    processing = True

    while task_queue:
        chat_id, reply_to_msg_id, file_start_param = task_queue.popleft()
        logger.info(f"Processing: {file_start_param} for chat: {chat_id}")

        status_msg = await bot.send_message(
            chat_id,
            "⏳ Fetching your file...",
            reply_to_message_id=reply_to_msg_id,
        )

        result_msg = await fetch_file_from_uploadpilot(file_start_param)

        if result_msg:
            try:
                await result_msg.copy(chat_id, reply_to_message_id=reply_to_msg_id)
                await status_msg.delete()
                logger.info(f"Delivered: {file_start_param} to {chat_id}")
            except Exception as e:
                await status_msg.edit(f"❌ Forward failed: `{e}`")
                logger.error(f"Forward error: {e}")
        else:
            await status_msg.edit("❌ Could not fetch file. Try again.")

        if task_queue:
            await asyncio.sleep(1)

    processing = False


# ─── Bot Handlers ──────────────────────────────────────────────────────────────

# NO group filter — koi bhi group/DM/channel mein use ho sakta hai
@bot.on_message(filters.forwarded)
async def handle_forwarded_message(client: Client, message: Message):
    """
    Koi bhi forwarded message. Sirf PEHLE button ka file_id lo.
    No restrictions — koi bhi use kar sakta hai.
    """
    file_id = extract_first_file_id(message)

    if not file_id:
        return

    logger.info(f"Queuing: {file_id} from chat {message.chat.id}")
    task_queue.append((message.chat.id, message.id, file_id))

    global processing
    if not processing:
        asyncio.create_task(process_queue())


@bot.on_message(filters.command("queue"))
async def show_queue(client: Client, message: Message):
    size = len(task_queue)
    status = "🔄 Processing" if processing else "✅ Idle"
    await message.reply(f"**Queue:** {status}\n**Pending:** {size} task(s)")


@bot.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    await message.reply(
        "👋 **Alternative Extractor Bot**\n\n"
        "UploadPilotBot buttons wala koi bhi message forward karo — "
        "main automatically **pehli quality** ka video/PDF de dunga!\n\n"
        "**Commands:**\n"
        "/queue — Queue status\n\n"
        "⚡ No restrictions. Koi bhi group, koi bhi user!"
    )
