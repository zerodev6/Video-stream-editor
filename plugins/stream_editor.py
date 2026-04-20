import os, time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from helpers.ffmpeg_utils import get_streams, map_streams
from helpers.progress import progress_bar
from config import Config
from plugins.force_sub import check_subscription

# Dictionary to store user selections
user_data = {}

@Client.on_message((filters.video | filters.document) & filters.private)
async def video_handler(client, message):
    if not await check_subscription(client, message):
        return
        
    from main import user_bot 
    
    msg = await message.reply("⚡ **Downloading to Server... Please wait.**", quote=True)
    
    try:
        file_path = await user_bot.download_media(
            message, 
            progress=progress_bar, 
            progress_args=("📥 Downloading...", msg, time.time())
        )
    except Exception as e:
        return await msg.edit(f"❌ **Download Failed:** {e}")
    
    await msg.edit("⚙️ **Analyzing streams using FFprobe...**")
    streams = await get_streams(file_path)
    
    # Initialize session data
    user_data[message.from_user.id] = {"path": file_path, "selected": []}
    
    text = "**Index | Type | Lang | Codec**\n"
    buttons = []
    
    for s in streams:
        idx = str(s.get('index'))
        stype = s.get('codec_type', 'unknown')
        codec = s.get('codec_name', 'unknown')
        lang = s.get('tags', {}).get('language', 'N/A')
        
        text += f"`{idx} | {stype.upper()} | {lang} | {codec}`\n"
        buttons.append([InlineKeyboardButton(f"Select {idx} ({stype})", callback_data=f"select_{idx}")])

    buttons.append([InlineKeyboardButton("📤 Process & Upload", callback_data="upload_final")])
    await msg.edit(text, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex(r"^select_(.*)"))
async def handle_selection(client, cb):
    user_id = cb.from_user.id
    stream_idx = cb.data.split("_")[1]
    
    if user_id not in user_data:
        return await cb.answer("❌ Session expired. Please resend the video.", show_alert=True)

    if stream_idx in user_data[user_id]["selected"]:
        user_data[user_id]["selected"].remove(stream_idx)
        await cb.answer(f"❌ Stream {stream_idx} removed from export list")
    else:
        user_data[user_id]["selected"].append(stream_idx)
        await cb.answer(f"✅ Stream {stream_idx} added to export list")


@Client.on_callback_query(filters.regex("^upload_final$"))
async def handle_upload(client, cb):
    user_id = cb.from_user.id
    data = user_data.get(user_id)
    
    if not data or not data["selected"]:
        return await cb.answer("⚠️ You must select at least one stream to keep!", show_alert=True)

    await cb.message.edit("⚙️ **Processing and filtering streams...**")
    
    input_file = data["path"]
    output_file = f"downloads/edited_{user_id}.mkv"
    os.makedirs("downloads", exist_ok=True)
    
    # Map streams using FFmpeg
    await map_streams(input_file, output_file, data["selected"])
    
    from main import user_bot
    await cb.message.edit("📤 **Uploading edited file...**")
    
    try:
        await user_bot.send_document(
            chat_id=cb.message.chat.id,
            document=output_file,
            caption="✅ **Stream Editing Complete!**\nUnselected streams were successfully removed.",
            progress=progress_bar,
            progress_args=("📤 Uploading...", cb.message, time.time())
        )
        await cb.message.delete()
    except Exception as e:
        await cb.message.edit(f"❌ **Upload Failed:** {e}")
    
    # Final cleanup of server storage
    if os.path.exists(input_file): os.remove(input_file)
    if os.path.exists(output_file): os.remove(output_file)
    if user_id in user_data: del user_data[user_id]
