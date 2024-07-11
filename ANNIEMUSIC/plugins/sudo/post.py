from pyrogram import filters
from ANNIEMUSIC import app
from config import OWNER_ID
from pyrogram.types import Message




@app.on_message(filters.command(["post"], prefixes=["/", "."]) & filters.user(OWNER_ID))
async def copy_messages(client, message: Message):
    if message.reply_to_message:
        command_parts = message.text.split()
        
        if len(command_parts) == 2:
            try:
                
                destination_group_id = int(command_parts[1])
                
                 
                await message.reply_to_message.copy(destination_group_id)
                
                
                await message.reply("ᴘᴏsᴛ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴏɴᴇ")
            except ValueError:
                await message.reply("**Invalid destination ID.**\nPlease provide a valid integer ID. Or Promote Me As Admin in`{destination_group_id}`")
        else:
            await message.reply("**Usage:**\n`/post` -1002200810390")
    else:
        await message.reply("Please reply to the message you want to post.")

