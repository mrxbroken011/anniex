import requests
from ANNIEMUSIC import app
import time
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from MukeshAPI import api

def reply_to_owner_query(query):
    recognized_queries = [
        "hello yumi who is your owner",
        "hello yumi tumhara malik kon h",
        "hello yumi who is your owner?",
        "hello yumi tumhara malik kon h?"
    ]
    
    normalized_query = query.strip().lower()
    
    if normalized_query in recognized_queries:
        response = {
            "message": ("My Owner Name is Mr Broken. You Can Call Him Broken also.\n"
                        "मेरा मालिक का नाम Broken है। आप उनको सिर्फ broken भी कह सकते हैं।")
        }
    else:
        response = {
            "message": "Message not recognized."
        }
    
    return response

@app.on_message(filters.command(["chatgpt", "ai", "ask", "arvis", "umi"], prefixes=[".", "J", "j", "y", "Y", "/"]))
async def chat_gpt(bot, message):
    try:
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        
        # Check if name is defined, if not, set a default value
        name = message.from_user.first_name if message.from_user else "User"
        
        if len(message.command) < 2:
            await message.reply_text(f"𝐇𝐞𝐥𝐥𝐨! {name}, 𝐇𝐨𝐰 𝐂𝐚𝐧 𝐈 𝐇𝐞𝐥𝐩 𝐘𝐨𝐮 𝐓𝐨𝐝𝐚𝐲?")
        else:
            query = message.text.split(' ', 1)[1]
            
            # Check for owner query
            owner_response = reply_to_owner_query(query)
            if owner_response["message"] != "Message not recognized.":
                await message.reply_text(
                    f"{owner_response['message']}\nᴀɴsᴡᴇʀɪɴɢ ʙʏ ➛  @Miss_YumiPro_Bot \nᴀsᴋᴇᴅ ʙʏ ➛ {name}", 
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                # Use the external API for other queries
                response = api.gemini(query)["results"]
                await message.reply_text(
                    f"{response}\nᴀɴsᴡᴇʀɪɴɢ ʙʏ ➛  @Miss_YumiPro_Bot \nᴀsᴋᴇᴅ ʙʏ ➛ {name}", 
                    parse_mode=ParseMode.MARKDOWN
                )
    except Exception as e:
        await message.reply_text(f"**Error: {e}**")
