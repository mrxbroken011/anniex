from pyrogram import Client, filters
from pyrogram.types import Message
import aiohttp
from ANNIEMUSIC import app

async def fetch_cc(bin):
    url = f"https://api.nophq.cc/gen/{bin}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"Failed to fetch data: {response.status}")

@app.on_message(filters.command(["gen", "ccgen"], [".", "!", "/"]))
async def gen_cc(client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**Please Give Me a Bin To\nGenerate Cc ...**")

    try:
        await message.delete()
    except:
        pass

    aux = await message.reply_text("**Generating ...**")
    bin = message.text.split(None, 1)[1]

    if len(bin) < 6:
        return await aux.edit("**❌ Wrong Bin❗...**")

    try:
        resp = await fetch_cc(bin)
        cards = resp['liveCC']

        await aux.edit(f"""
**sᴏᴍᴇ ʟɪᴠᴇ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴄᴄ 💳:**

`{cards[0]}`\n`{cards[1]}`\n`{cards[2]}`
`{cards[3]}`\n`{cards[4]}`\n`{cards[5]}`
`{cards[6]}`\n`{cards[7]}`\n`{cards[8]}`
`{cards[9]}`

**💳 Bin:** `{resp['bin']}`
**⏳ Time Took:** `{resp['took']}`\n\n"""
        )
    except Exception as e:
        return await aux.edit(f"**Error:** `{e}`")

# Modified API (MR_BROKEN) 
