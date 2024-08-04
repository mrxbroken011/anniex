#© MR Broken

from ... import *
from pyrogram import *
from pyrogram.types import *
import random
from config import OWNER_USERNAME



def luhn_algorithm(cc_num):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(cc_num)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10 == 0

def generate_luhn_valid_cc(bin, length):
    cc_number = [int(x) for x in bin]
    while len(cc_number) < (length - 1):
        cc_number.append(random.randint(0, 9))
    checksum = 0
    cc_number.append(checksum)
    for i in range(length - 2, -1, -2):
        cc_number[i] *= 2
        if cc_number[i] > 9:
            cc_number[i] -= 9
    checksum = (10 - (sum(cc_number) % 10)) % 10
    cc_number[-1] = checksum
    return ''.join(map(str, cc_number))

@app.on_message(filters.command(["gen", "ccgen"], [".", "!", "/"]))
async def gen_cc(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "**🔔ᴘʟᴇᴀsᴇ ɢɪᴠᴇ ᴍᴇ ᴀ ʙɪɴ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴄᴄ ...💳**\n `/gen 123456`"
        )
    try:
        await message.delete()
    except:
        pass
    aux = await message.reply_text("** ɢᴇɴᴇʀᴀᴛɪɴɢ...☢️**")
    bin = message.text.split(None, 1)[1]
    if len(bin) < 6:
        return await aux.edit("**🚫 ᴡʀᴏɴɢ ʙɪɴ ⚠️...**")
    try:
        
        cards = [generate_luhn_valid_cc(bin, 16) for _ in range(10)]
        await aux.edit(f"""
❅─────────✧❅𝗕𝗥𝗢𝗞𝗘𝗡 𝗫 𝗖𝗖 𝗚𝗘𝗡𝗘𝗥𝗔𝗧𝗢𝗥❅✧─────────❅

`{cards[0]}`\n`{cards[1]}`\n`{cards[2]}`
`{cards[3]}`\n`{cards[4]}`\n`{cards[5]}`
`{cards[6]}`\n`{cards[7]}`\n`{cards[8]}`
`{cards[9]}`


**⚠️ ᴀʟɢᴏʀɪᴛʜᴍ: Luhn**

**🪪 ᴅᴇᴠ:** @{OWNER_USERNAME}

**💳 ʙɪɴ:** `{bin}`

**⏳ ᴛɪᴍᴇ ᴛᴏᴏᴋ:** `-`\n\n"""
        )
    except Exception as e:
        return await aux.edit(f"**Error:** `{e}`")

