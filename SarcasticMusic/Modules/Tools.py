import os
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from SarcasticMusic import app, Ass, BOT_NAME, SUDO_USERS
from SarcasticMusic.Helpers.Database import get_active_chats


__MODULE__ = "Tools"
__HELP__ = """

**Note :**
Only for sudoers


/joinassistant [chat username/id]
» order the assistant to join that chat.

/leaveassistant [chat username/id]
» order the assistant to leave that chat.

/leavebot [chat username/id]
» order the bot to leave that chat.

(✿◠‿◠)
"""


@app.on_message(filters.command(["activevc", "activevoice"]) & filters.user(SUDO_USERS))
async def activevc(_, message: Message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        await message.reply_text(f"**Error :** {e}")
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "Private group"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += (
                f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n\n"
            )
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n\n"
        j += 1
    if not text:
        await message.reply_text(f"**» No active voice-chat on {BOT_NAME} server.**")
    else:
        await message.reply_text(
            f"**» Active voice chat on {BOT_NAME} server :**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["joinassistant", "join", "ass", "assistant"]) & filters.user(SUDO_USERS))
async def assjoin(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**Example :**\n/joinassistant [chat username/id]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await Ass.join_chat(chat)
    except Exception as e:
        await message.reply_text(f"Failed.\n\n**Reason :** {e}")
        return
    await message.reply_text("**» Sucessfully joined that chat.**")


@app.on_message(filters.command(["leavebot", "leave"]) & filters.user(SUDO_USERS))
async def botl(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**Example :**\n/leavebot [chat username or id]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await app.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"Failed\n**Reason :** {e}")
        print(e)
        return
    await message.reply_text("**» Sucessfully leave that chutiya's group.**")


@app.on_message(filters.command(["leaveassistant", "assleave", "userbotleave", "leaveass"]) & filters.user(SUDO_USERS))
async def assleave(_, message):
    if len(message.command) != 2:
        await message.reply_text(
            "**Example :**\n/assleave [chat username or id]"
        )
        return
    chat = message.text.split(None, 2)[1]
    try:
        await Ass.leave_chat(chat)
    except Exception as e:
        await message.reply_text(f"Failed\n**Reason :** {e}")
        return
    await message.reply_text("**» Assistant sucessfully leave that chutiya's group**")
