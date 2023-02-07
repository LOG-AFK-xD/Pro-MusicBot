import os
import asyncio

from pyrogram import filters
from pyrogram.types import Message

from SarcasticMusic import BOT_NAME, OWNER_ID, app
from SarcasticMusic.Helpers.Database import add_off, add_on


__MODULE__ = "Maintenance"
__HELP__ = """

**Note :**
Only for sudo-users ✨


/maintenance on
» enable the maintanence mode of the bot.

/maintenance off
» disable the maintanence mode of the bot.
"""


@app.on_message(filters.command("maintenance") & filters.user(OWNER_ID))
async def maintenance(_, message):
    exp = "**Example :**\n/maintenance [on|off]"
    if len(message.command) != 2:
        return await message.reply_text(exp)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "on":
        user_id = 1
        await add_on(user_id)
        await message.reply_text(f"**» {BOT_NAME} maintenance mode enabled sucessfully 🙂**")
    elif state == "off":
        user_id = 1
        await add_off(user_id)
        await message.reply_text(f"**» {BOT_NAME} maintenance mode disabled 👀**")
    else:
        await message.reply_text(exp)
