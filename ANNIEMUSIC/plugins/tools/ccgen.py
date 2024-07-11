from ... import *
from pyrogram import *
from pyrogram.types import *

import aiohttp


async def fetch_cc(bin, quantity):
    url = f"https://api.nophq.cc/gen/{bin}/{quantity}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to fetch data: {response.status}")

@app.on_message(filters.command(["gen", "ccgen"], [".", "!", "/"]))
async def gen_cc(client: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply_text(
            "**Please provide a BIN and quantity to generate CCs.**\nExample: /gen 123456 10"
        )

    try:
        await message.delete()
    except Exception as e:
        print(f"Failed to delete message: {e}")

    aux = await message.reply_text("**Generating ...**")
    bin = message.command[1]
    quantity = message.command[2]

    if len(bin) < 6:
        return await aux.edit("**❌ Wrong BIN❗...**")
    
    try:
        quantity = int(quantity)
        if quantity <= 0:
            return await aux.edit("**❌ Quantity must be a positive number.**")
    except ValueError:
        return await aux.edit("**❌ Quantity must be a number.**")

    try:
        
        resp = await fetch_cc(bin, quantity)

        
        if 'liveCC' not in resp or not resp['liveCC']:
            return await aux.edit("**Failed to generate CC.**")

        cards = resp['liveCC']

        
        filename = "miss_yumipro_bot_cc.txt"
        with open(filename, 'w') as f:
            for card in cards:
                f.write(f"{card}\n")

        await aux.edit(f"**sᴏᴍᴇ ʟɪᴠᴇ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴄᴄ 💳 ({quantity}):**\n\n" +
                       "\n".join([f"`{card}`" for card in cards[:10]]) +  
                       f"\n\n**💳 Bin:** `{resp['bin']}`"
                       f"\n**⏳ Time Took:** `{resp['took']}`\n\n" +
                       f"**✅ Saved to:** `{filename}`")

        
        await message.reply_document(document=InputFile(filename))

    except Exception as e:
        await aux.edit(f"**Error:** `{e}`")
        print(f"Error generating CC: {e}")
