import os
import config
import asyncio

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from SarcasticMusic import BOT_ID, BOT_NAME, SUDO_USERS, app
from SarcasticMusic.Helpers.Database import (add_gban_user, get_served_chats, is_gbanned_user, remove_gban_user)


__MODULE__ = "Global-ban"
__HELP__ = """

**Note :**
Only for sudo-users ✨

/gban [username or reply to a user]
» globally ban the user from all the chat where this bot served.

/ungban [username or reply to a user]
» globally unbans the user.
"""


@app.on_message(filters.command("gban") & filters.user(SUDO_USERS))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**Example :**\n/gban [username|user id]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            return await message.reply_text(
                "**» you can't g-ban your self my babu !**"
            )
        elif user.id == BOT_ID:
            await message.reply_text("» Shut up, you want me to gban myself, go and fuck off yaar !")
        elif user.id in SUDO_USERS:
            await message.reply_text("» Are you idiot i can't gban my baby and babu log if you do this same i will kill you babes 🙂🥀")
        else:
            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Globally banning {user.mention}**\n\nExpected time : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
**Global ban on {BOT_NAME}**

**• Chat :** {message.chat.title} [`{message.chat.id}`]
**• Sudoer :** {from_user.mention}
**• User :** {user.mention}
**• User-id:** `{user.id}`
**• Banned in :** {number_of_chats} chats"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id == from_user_id:
        await message.reply_text("» You can't gban yourself babes !")
    elif user_id == BOT_ID:
        await message.reply_text("» You want me to ban mysel, huh bloody noob 🙂")
    elif user_id in SUDO_USERS:
        await message.reply_text("»  Are you idiot i can't gban my baby and babu log if you do this same i will kill you babes 🙂🥀")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("**Already gbanned that idiot now shoul i f*ck him ..!?**")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Globally banning {mention}**\n\nExpected time : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
**Global ban on {BOT_NAME}**

**• Chat :** {message.chat.title} [`{message.chat.id}`]
**• Sudoer :** {from_user_mention}
**• User :** {mention}
**• User-id :** `{user_id}`
**• Banned in :** {number_of_chats} chats"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("ungban") & filters.user(SUDO_USERS))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**Example :**\n/ungban [username|user-id]"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            await message.reply_text("» I already tell you you can't g-ban your self so how the fuck you can ungban your self 😐")
        elif user.id == BOT_ID:
            await message.reply_text("» You bloody noob, you don't have aukat to gban me so how you ungban me..kid ..!?")
        elif user.id in SUDO_USERS:
            await message.reply_text("» Read this statement last time, i'm not gonna tell you again and again that you can't gban my baby 😐😅")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("» This user isn't gbanned 🙂")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"» Removed from gbanned list...")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id == from_user_id:
        await message.reply_text("» I already tell you you can't g-ban your self so how the fuck you can ungban your self 😐")
    elif user_id == BOT_ID:
        await message.reply_text(
            "» You bloody noob, you don't have aukat to gban me so how you ungban me..kid ..!?"
        )
    elif user_id in SUDO_USERS:
        await message.reply_text("» Read this statement last time, i'm not gonna tell you again and again that you can't gban my baby 😐😅")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("» This user isn't g-banned !")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"» Removed from gbanned user list...")



chat_watcher_group = 5

@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    try:
        userid = message.from_user.id
    except Exception:
        return
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.kick_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"{checking} is gbanned on {BOT_NAME}\n\n**Reason :** He is chutiya, suwar and paltu kutta of bises and hopper ji 🙂"
        )
