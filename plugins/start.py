import random, string, asyncio, os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pytz
from datetime import datetime

from config import Config
from helpers.database import db
from script import START_TXT, HELP_TXT
from plugins.force_sub import check_subscription

PICS_URL = ["https://api.aniwallpaper.workers.dev/random?type=girl"]

def get_random_mix_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def get_greeting():
    hour = datetime.now(pytz.timezone('Asia/Kolkata')).hour
    if hour < 12: return "Good Morning ☀️"
    elif hour < 17: return "Good Afternoon 🌤️"
    else: return "Good Evening 🌙"

@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):
    if not await check_subscription(client, message):
        return
    
    await db.add_user(message.from_user.id)
    
    # Send temporary sticker
    sticker = await message.reply_sticker("CAACAgIAAxkBAAEQZtFpgEdROhGouBVFD3e0K-YjmVHwsgACtCMAAphLKUjeub7NKlvk2TgE")
    await asyncio.sleep(2)
    await sticker.delete()

    welcome_img = f"{random.choice(PICS_URL)}?r={get_random_mix_id()}"
    await message.reply_photo(
        photo=welcome_img,
        caption=START_TXT.format(message.from_user.first_name, get_greeting()),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Help 🛠️", callback_data="help_data")]])
    )

@Client.on_message(filters.command("info") & filters.private)
async def info_handler(client, message):
    user = message.from_user
    text = f"""
➲ **First Name:** {user.first_name}
➲ **Last Name:** {user.last_name or 'None'}
➲ **Telegram ID:** `{user.id}`
➲ **Data Centre:** {user.dc_id or 'Unknown'}
➲ **User Name:** @{user.username or 'None'}
➲ **User Link:** [Click Here](tg://user?id={user.id})
    """
    if user.photo:
        photo = await client.download_media(user.photo.big_file_id)
        await message.reply_photo(photo, caption=text)
        if os.path.exists(photo): os.remove(photo) # Clean up temp profile pic
    else:
        await message.reply_text(text)

@Client.on_callback_query(filters.regex("^help_data$"))
async def help_callback(client, cb):
    await cb.message.edit_caption(
        caption=HELP_TXT,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_start")]])
    )

@Client.on_callback_query(filters.regex("^back_start$"))
async def back_callback(client, cb):
    await cb.message.edit_caption(
        caption=START_TXT.format(cb.from_user.first_name, get_greeting()),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Help 🛠️", callback_data="help_data")]])
)
  
