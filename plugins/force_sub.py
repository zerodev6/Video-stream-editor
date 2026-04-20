from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant
from config import Config

async def check_subscription(client, message):
    if not Config.FORCE_SUB_CHANNELS:
        return True
    
    user_id = message.from_user.id
    not_joined = []
    
    for channel in Config.FORCE_SUB_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            not_joined.append(channel)
        except Exception:
            pass # Ignore if bot is not admin in the channel
            
    if not_joined:
        buttons = [[InlineKeyboardButton("Join Channel ➡️", url=f"https://t.me/{c}")] for c in not_joined]
        buttons.append([InlineKeyboardButton("✅ I've Joined", callback_data="check_sub")])
        
        await message.reply_text(
            "🚫 **Access Denied!**\n\nYou must join our updates channels to use this bot.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return False
    return True

@Client.on_callback_query(filters.regex("^check_sub$"))
async def check_sub_callback(client, cb):
    user_id = cb.from_user.id
    not_joined = []
    
    for channel in Config.FORCE_SUB_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            not_joined.append(channel)
        except Exception:
            pass
            
    if not_joined:
        await cb.answer("❌ You haven't joined all channels yet!", show_alert=True)
    else:
        await cb.message.delete()
        await client.send_message(cb.message.chat.id, "✅ **Thank you for joining!**\n\nSend /start to continue.")
