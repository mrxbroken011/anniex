import asyncio
import requests
from ANNIEMUSIC import app
from pyrogram import filters
from pyrogram.enums import ChatAction, MessageEntityType

@app.on_message(filters.text, group=30)
async def ai_chat_bot(client, message):
    chat_id = message.chat.id
    if message.sender_chat:
        user_id = message.sender_chat.id
    else:
        user_id = message.from_user.id

    if message.entities:
        for entity in message.entities:
            if entity.type == MessageEntityType.BOT_COMMAND:
                return
    
    replied = message.reply_to_message
    if replied:
        if replied.from_user.id != app.id:
            return
    
    await client.send_chat_action(chat_id, ChatAction.TYPING)
    await asyncio.sleep(3)
    
    url = "https://create-chatbot.p.rapidapi.com/api/v1/text/generate"
    headers = {
        'X-RapidAPI-Key': 'Iq7MGR1dZAmshgT7vWvmTFsBGOP2p1IxZw3jsnBmLfKXgwKR9Z',
        'Content-Type': 'application/json'
    }
    payload = {
        'text': message.text,
        'source': 'telegram'
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        result = response.json()
        
        if 'response' in result:
            answer = result['response']
            await message.reply_text(answer)
        else:
            await message.reply_text("**Sorry, I couldn't. Please ask** @MrBrokn **To Add API KEY**")
    
    except requests.exceptions.RequestException as e:
        await message.reply_text(f"Request failed: {e}")
    
    await client.send_chat_action(chat_id, ChatAction.CANCEL)
