import asyncio, requests

from ANNIEMUSIC import app
import config
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
        for x in message.entities:
            if x.type == MessageEntityType.BOT_COMMAND:
                return
    replied = message.reply_to_message
    if replied:
        if replied.from_user.id == app.id:
            pass
        else:
            return
    await client.send_chat_action(chat_id, ChatAction.TYPING)
    await asyncio.sleep(3)
    url = "https://api.deepai.org/api/text-generator"
    headers = {
        'Api-Key': config.DEEP_API
    }
    data = {
        'text': message.text
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        answer = response.json()['output']
        return await message.reply_text(answer)
    return await client.send_chat_action(chat_id, ChatAction.CANCEL)
