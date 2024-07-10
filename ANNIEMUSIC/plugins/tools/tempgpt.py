import requests
from ANNIEMUSIC import app
import time
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from MukeshAPI import api

@app.on_message(filters.command(["chatgpt", "ai", "ask", "arvis", "umi"], prefixes=[".", "J", "j", "y", "Y", "/"]))
async def chat_gpt(bot, message):
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        # Check if name is defined, if not, set a default value
        name = message.from_user.first_name if message.from_user else "User"
        
        if len(message.command) < 2:
            await message.reply_text(f"𝐇𝐞𝐥𝐥𝐨! {name}, 𝐇𝐨𝐰 𝐂𝐚𝐧 𝐈 𝐇𝐞𝐥𝐩 𝐘𝐨𝐮 𝐓𝐨𝐝𝐚𝐲? ")
        else:
            query = message.text.split(' ', 1)[1]
            response = api.gemini(query)["results"]
            await message.reply_text(
                f"{response}\nᴀɴsᴡᴇʀɪɴɢ ʙʏ ➛  @Miss_YumiPro_Bot \nᴀsᴋᴇᴅ ʙʏ ➛ {name} ", 
                parse_mode=ParseMode.MARKDOWN
            )
    except Exception as e:
        await message.reply_text(f"**Error: {e}**")
