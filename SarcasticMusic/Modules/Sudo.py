import os
import asyncio
import subprocess

from pyrogram import filters
from pyrogram.types import Message

from SarcasticMusic import BOT_NAME, OWNER_ID, SUDO_USERS, app
from SarcasticMusic.Helpers.Database import (get_active_chats, get_served_chats, remove_active_chat)


__MODULE__ = "Sudo-Users"
__HELP__ = """

/sudolist 
» shows the list of sudoers.


**Note :**
Only for sudo-users ✨

/restart 
» restart the bot on your server

/update 
» fetch update from the repo.

/clean
» clean all the temp directories.

(✿◠‿◠)
"""


@app.on_message(filters.command(["sudolist", "listsudo", "sudo", "owner"]))
async def sudoers_list(_, message: Message):
    sudoers = SUDO_USERS
    text = "<u>✨ **Owner :**</u>\n"
    wtf = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = user.first_name if not user.mention else user.mention
            wtf += 1
        except Exception:
            continue
        text += f"{wtf}➻ {user}\n"
    smex = 0
    for count, user_id in enumerate(sudoers, 1):
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n💡<u> **Sudoers :**</u>\n"
                wtf += 1
                text += f"{wtf}➻ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("**» No sudo users found for the bot ✨**")
    else:
        await message.reply_text(text)



## Restart

@app.on_message(filters.command("restart") & filters.user(OWNER_ID))
async def theme_func(_, message):
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        pass
    for x in served_chats:
        try:
            await app.send_message(
                x,
                f"» {BOT_NAME} just restarted for fetching updated from repo.\n\nSorry for inconvience (✿◡‿◡)",
            )
            await remove_active_chat(x)
        except Exception:
            pass
    x = await message.reply_text(f"**Restarting {BOT_NAME}\n\nPlease wait...**")
    os.system(f"kill -9 {os.getpid()} && python3 -m SarcasticMusic")



## Update

@app.on_message(filters.command("update") & filters.user(SUDO_USERS))
async def update(_, message):
    m = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if str(m[0]) != "A":
        x = await message.reply_text("**» Fetching update from repo and trying to restart...**")
        return os.system(f"kill -9 {os.getpid()} && python3 -m SarcasticMusic")
    else:
        await message.reply_text(f"**» {BOT_NAME} is already up-2-date !**")



## Broadcast

@app.on_message(filters.command("broadcast") & filters.user(SUDO_USERS))
async def broadcast(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"**Sucessfully broadcasted the message in {sent} chats.**")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Example :**\n/broadcast [message] or [reply to a message]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"**» Sucessfully broadcasted message in {sent} chats.**")



@app.on_message(filters.command("broadcast_pin") & filters.user(SUDO_USERS))
async def broadcast_message_pin_silent(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**» Broadcasted message in {sent} chats and pinned in {pin} chats.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Example :**\n/broadcast [message] or [reply to a message]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=False)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**» Broadcasted message in {sent} chats and pinned in {pin} chats.**"
    )


# Clean

@app.on_message(filters.command("clean") & filters.user(SUDO_USERS))
async def clean(_, message):
    dir = "SarcasticMusic/Cache"
    ls_dir = os.listdir(dir)
    if ls_dir:
        for dta in os.listdir(dir):
            os.system("rm -rf *.png *.jpg")
        await message.reply_text("**» Sucessfully cleaned up all temporary directories!**")
    else:
        await message.reply_text("**» Sucessfully cleaned up all temporary directories**")
