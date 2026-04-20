import os, time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from helpers.ffmpeg_utils import get_streams, map_streams
from helpers.progress import progress_bar
from config import Config

# Dictionary to store user choices (temporary)
user_data = {}

@Client.on_message((filters.video | filters.document) & filters.private)
async def video_handler(client, message):
    # Use user_bot (Admin session) to download files up to 4GB
    from main import user_bot 
    
    msg = await message.reply("⚡ **Processing file... Please wait.**")
    file_path = await user_bot.download_media(
        message, 
        progress=progress_bar, 
        progress_args=("📥 Downloading...", msg, time.time())
    )
    
    streams = await get_streams(file_path)
    user_data[message.from_user.id] = {"path": file_path, "selected": []}
    
    text = "**Index | Type | Lang | Codec**\n"
    buttons = []
    for s in streams:
        idx, stype, codec = s.get('index'), s.get('codec_type'), s.get('codec_name')
        lang = s.get('tags', {}).get('language', 'N/A')
        text += f"`{idx} | {stype.upper()} | {lang} | {codec}`\n"
        buttons.append([InlineKeyboardButton(f"Select {idx} ({stype})", callback_data=f"select_{idx}")])

    buttons.append([InlineKeyboardButton("📤 Upload Video", callback_data="upload_final")])
    await msg.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
