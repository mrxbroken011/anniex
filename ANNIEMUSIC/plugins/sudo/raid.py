import pyrogram
import time
from pyrogram import filters
from pyrogram import Client
from ANNIEMUSIC import app
from ANNIEMUSIC.misc import SUDOERS

# Define the spam command handler
@app.on_message(filters.command("raid", prefixes=".") & SUDOERS)
def spam_command(client, message):
    try:
        # Delete the user's command text
        message.delete()
    except pyrogram.errors.exceptions.FloodWait as e:
        print(f"Error deleting message: {e}")
        pass  # Ignore the deletion error and continue

    # Check if the message is a reply and has text
    if message.reply_to_message:
        user_to_tag = message.reply_to_message.from_user.mention()
        command_args = message.text.split(" ", 2)[1:]

        if len(command_args) == 2:
            try:
                num_times = int(command_args[1])
                text_to_spam = command_args[0]
            except ValueError:
                message.reply_text("**Invalid number format for amount.**\n**Usage:** .raid <text> <amount>")
                return
        else:
            message.reply_text("**Incorrect usage.**\n**Usage:** .raid <text> <amount>")
            return

        for _ in range(num_times):
            # Send the spam message to the Telegram chat and mention the user
            message.reply_text(f"{user_to_tag} **{text_to_spam}**")
            time.sleep(0.5)  # Add a delay between spam messages
    else:
        message.reply_text("**Reply to a message and use the .raid command to spam.**\n**Usage:** .raid <text> <amount>")
