from pyrogram import Client, filters
from config import Config
from helpers.database import db

@Client.on_message(filters.command("stats") & filters.user(Config.ADMINS))
async def stats_handler(client, message):
    total = await db.get_total_users()
    await message.reply(f"📊 **Bot Stats**\n\nTotal Users: {total}")

@Client.on_message(filters.command("broadcast") & filters.user(Config.ADMINS))
async def broadcast_handler(client, message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")
    
    users = await db.get_all_users()
    count = 0
    async for user in users:
        try:
            await message.reply_to_message.copy(user['id'])
            count += 1
        except:
            pass
    await message.reply(f"✅ Broadcast sent to {count} users.")
  
