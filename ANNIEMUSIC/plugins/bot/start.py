import asyncio
import random
import time
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from ANNIEMUSIC import app
from ANNIEMUSIC.misc import _boot_
from ANNIEMUSIC.plugins.sudo.sudoers import sudoers_list
from ANNIEMUSIC.utils import bot_sys_stats
from ANNIEMUSIC.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    get_served_chats,
    get_served_users,
    is_banned_user,
    is_on_off,
)
from ANNIEMUSIC.utils.decorators.language import LanguageStart
from ANNIEMUSIC.utils.formatters import get_readable_time
from ANNIEMUSIC.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS, AYUV
from strings import get_string

ANNIE_VID = [
    "https://telegra.ph/file/c1245469a992ed7eea832.jpg", 
    "https://telegra.ph/file/9cea0b7593c411edfff53.jpg", 
    "https://telegra.ph/file/5ce1e15afb0c7e9d17fff.jpg",
    "https://telegra.ph/file/314badfb74642e96240f5.jpg",
    "https://telegra.ph/file/235e85ae81c8ee40f7b64.jpg", 
    "https://telegra.ph/file/c2dfd1a9bda7e9e774541.jpg",
    "https://telegra.ph/file/70669bef810e52545bb10.jpg", 
    "https://telegra.ph/file/aaea0abbc1bbeb9c03ba8.jpg",
    "https://telegra.ph/file/d55b8833e9f93ee6afbcc.jpg", 
    "https://telegra.ph/file/c7907b3302dc5ad379a06.jpg", 
    "https://telegra.ph/file/c68e5d503614f748d82e7.jpg", 
    "https://telegra.ph/file/e10a6b780005047756222.jpg", 
    "https://telegra.ph/file/91bac150fd50d7d9fdd90.jpg", 
    "https://telegra.ph/file/bc8adc47b217e8574cc14.jpg",
    "https://telegra.ph/file/21488284d02bad2e0668e.jpg", 
    "https://telegra.ph/file/3d4580aa35deaa45a9f44.jpg", 
    "https://telegra.ph/file/92a67bd139d5eb7e462bd.jpg", 
    "https://telegra.ph/file/503779919c8b4183a783d.jpg", 
    "https://telegra.ph/file/a4cb485d162d69037b630.jpg", 
    "https://telegra.ph/file/ca3c86842fe3a4f07a3b6.jpg", 
    "https://telegra.ph/file/69e9522016014d6838ad3.jpg", 
]

STICKERS = [
    "CAACAgUAAxkBAAIGgGZ-FKBKqmFPfCvY_r5Rv5QHgCZXAAJrDwACUyI5V0DyywS65FCUHgQ",
    "CAACAgUAAxkBAAIBeWaUVgc_0Y6gvSkE5HaBAbNxeJICAALSEAACuJ_QVr0Lp98DEI3aHgQ", 
    "CAACAgUAAxkBAAIBfWaUVmouyzVy-LjrwVLn9VIciYhfAAKhDwACUIrgVt-ivr3brFblHgQ", 
    "CAACAgUAAxkBAAIBgWaUVvCT9ufK9dzrFfe0lyTuYWnxAAJOEAACDaO4VvnA5DcxZtBaHgQ", 
    "CAACAgUAAxkBAAIBhWaUV3qP1UrpFgSDxc0ycJUaJtU9AALSEAACOBPhVulGhjrfijJSHgQ", 
]

async def delete_sticker_after_delay(message, delay):
    await asyncio.sleep(delay)
    await message.delete()

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            sticker_message = await message.reply_sticker(sticker=random.choice(STICKERS))
            asyncio.create_task(delete_sticker_after_delay(sticker_message, 5))  # Delete sticker after 2 seconds
            await message.reply_photo(
                random.choice(ANNIE_VID),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        elif name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
        elif name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = str(name).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                ]
            )
            await m.delete()
            await app.send_video(
                chat_id=message.chat.id,
                video=thumbnail,
                caption=searched_text,
                reply_markup=key,
            )
            if await is_on_off(2):
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
                )
    else:
        out = private_panel(_)
        sticker_message = await message.reply_sticker(sticker=random.choice(STICKERS))
        asyncio.create_task(delete_sticker_after_delay(sticker_message, 2))  # Delete sticker after 2 seconds
        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        UP, CPU, RAM, DISK = await bot_sys_stats()
        await message.reply_photo(
            random.choice(ANNIE_VID),
            caption=random.choice(AYUV).format(message.from_user.mention, app.mention, UP, DISK, CPU, RAM, served_users, served_chats),
            reply_markup=InlineKeyboardMarkup(out),
        )
        if await is_on_off(2):
            await app.send_message(
                chat_id=config.LOGGER_ID,
                text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
            )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        random.choice(ANNIE_VID),
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_photo(
                    random.choice(ANNIE_VID),
                    caption=_["start_3"].format(
                        message.from_user.mention,
                        app.mention,
                        message.chat.title,
                        app.mention,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
