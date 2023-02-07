import time
import config
import asyncio
from typing import Dict, List, Union

from pyrogram import filters
from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, Message)

from SarcasticMusic import ASSID, BOT_NAME, BOT_USERNAME, OWNER_ID, SUDO_USERS, F_OWNER, app
from SarcasticMusic.Helpers.Database import (add_served_chat, add_served_user, is_served_chat, remove_active_chat)
from SarcasticMusic.Cache.permission import PermissionCheck
from SarcasticMusic.Helpers.Inline import start_pannel


welcome_group = 2

__MODULE__ = "Start"
__HELP__ = """

/start 
» start the bot.

/help 
» show the help menu of the bot.

(✿◠‿◠)
"""


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id == ASSID:
                return await remove_active_chat(chat_id)
            if member.id in OWNER_ID:
                return await message.reply_text(
                    f"**» ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ {BOT_NAME} ᴊᴜsᴛ ᴊᴏɪɴᴇᴅ ʏᴏᴜʀ ᴄʜᴀᴛ.**\n\n➻ ᴏᴡɴᴇʀ : [{member.mention}] 🥀"
                )
            if member.id in SUDO_USERS:
                return await message.reply_text(
                    f"**» ᴀ sᴜᴅᴏ ᴜsᴇʀ ᴏғ {BOT_NAME} ᴊᴜsᴛ ᴊᴏɪɴᴇᴅ ʏᴏᴜʀ ᴄʜᴀᴛ.**\n\n➻ sᴜᴅᴏᴇʀ : [{member.mention}] 🥀"
                )
                return
        except:
            return


@app.on_message(filters.command(["help", "start", f"start@{BOT_USERNAME}"]) & filters.group)
@PermissionCheck
async def gstart(_, message: Message):
    await asyncio.gather(
        message.delete(),
        message.reply_text(
            f"» Hey,\nThis is {BOT_NAME}\n A music player bot for telegram.\n\nThanks for adding me in {message.chat.title}.\n\nIf you have any question about me you can ask it in support chat ✨",
            reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="+ Add me to your clan +", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                ),
            ],
            [
                 InlineKeyboardButton(
                    text="✨ Support ✨", url=config.SUPPORT_CHAT
                ),
                InlineKeyboardButton(
                    text="❄ Help ❄", callback_data="sarcastic_help"
                ),
            ],
        ]
     ),
  )
)

