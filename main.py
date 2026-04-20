import asyncio
import datetime
import pytz
from pyrogram import Client, filters, idle
from config import Config
from helpers.database import db

# Bot Client
bot = Client(
    "StreamEditorBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="plugins")
)

# Admin User Client (For 4GB support)
user_bot = Client(
    "AdminSession",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    session_string=Config.ADMIN_SESSION_STRING
)

async def start_services():
    await bot.start()
    print("Bot Started!")
    await user_bot.start()
    print("User Client Started!")
    await idle()
    await bot.stop()
    await user_bot.stop()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_services())
  
