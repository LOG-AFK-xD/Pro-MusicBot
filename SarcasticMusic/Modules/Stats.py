import os
import re
import json
import uuid
import time
import psutil
import socket
import logging
import asyncio
import platform

from datetime import datetime
from sys import version as pyver
from pymongo import MongoClient

from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pyrogram.types import Message
from SarcasticMusic import (BOT_NAME, SUDO_USERS, app, Ass, StartTime, MONGO_DB_URI)
from SarcasticMusic.Helpers.Database import get_gbans_count, get_served_chats, get_served_users
from SarcasticMusic.Helpers.Inline import stats_f, stats_b
from SarcasticMusic.Modules import ALL_MODULES
from SarcasticMusic.Helpers.Ping import get_readable_time


__MODULE__ = "Stats"
__HELP__ = """

/stats
» show the system, assistant, bot and mongodb stats of bot

(✿◠‿◠)
"""


@app.on_message(filters.command(["stats", "gstats"]) & ~filters.edited)
async def gstats(_, message):
    try:
        await message.delete()
    except:
        pass
    hehe = await message.reply_photo(
        photo="SarcasticMusic/Utilities/Stats.jpg", caption=f"**» Pleasewait...\n\n• Getting {BOT_NAME} stats...**"
    )
    smex = f"""
**Choose an option for getting {BOT_NAME} general stats or assistant or overall stats of bot.**
    """
    await hehe.edit_text(smex, reply_markup=stats_f)
    return


@app.on_callback_query(
    filters.regex(
        pattern=r"^(sys_stats|bot_stats|get_back|mongo_stats|wait_stats)$"
    )
)
async def stats_markup(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    if command == "sys_stats":
        await CallbackQuery.answer("Getting system stats...")
        mod = len(ALL_MODULES)
        sc = platform.system()
        arch = platform.machine()
        p_core = psutil.cpu_count(logical=False)
        t_core = psutil.cpu_count(logical=True)
        ram = (
            str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " ɢʙ"
        )
        hdd = psutil.disk_usage("/")
        total = hdd.total / (1024.0 ** 3)
        total = str(total)
        used = hdd.used / (1024.0 ** 3)
        used = str(used)
        free = hdd.free / (1024.0 ** 3)
        free = str(free)
        bot_uptime = int(time.time() - StartTime)
        uptime = f"{get_readable_time((bot_uptime))}"
        smex = f"""
➻ <u>**{BOT_NAME} System stats :**</u>

• **Uptime :** {uptime}
• **Modules :** {mod}
• **Platform :** {sc}
• **Architecture :** {arch}
• **Physical core :** {p_core}
• **Total cores :** {t_core}
• **Ram :** {ram}
• **Python :** v{pyver.split()[0]}
• **Pyrogram :** v{pyrover}


➻ <u>**{BOT_NAME} Storage stats :**</u>

• **Total :** {total[:4]} gb
• **Used :** {used[:4]} gb
• **Free :** {free[:4]} gb

(✿◠‿◠)
"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats_b)
    if command == "bot_stats":
        await CallbackQuery.answer("Getting bot and assistant stats...")
        groups_ub = channels_ub = bots_ub = privates_ub = total_ub = 0
        async for i in Ass.iter_dialogs():
            t = i.chat.type
            total_ub += 1
            if t in ["supergroup", "group"]:
                groups_ub += 1
            elif t == "channel":
                channels_ub += 1
            elif t == "bot":
                bots_ub += 1
            elif t == "private":
                privates_ub += 1

        served_chats = len(await get_served_chats())
        served_users = len(await get_served_users())
        blocked = await get_gbans_count()
        sudoers = len(SUDO_USERS)
        mod = len(ALL_MODULES)
        smex = f"""
➻ <u>**{BOT_NAME} General stats :**</u>

• **Modules :** {mod}
• **Gbanned :** {blocked}
• **Sudoers :** {sudoers}
• **Chats :** {served_chats}
• **Users :** {served_users}

➻ <u>**{BOT_NAME} Assistant stats :**</u>

• **Total :** {total_ub}
• **Group :** {groups_ub}
• **Channels :** {channels_ub}
• **Bots :** {bots_ub}
• **Users :** {privates_ub}

(✿◠‿◠)
"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats_b)
    if command == "mongo_stats":
        await CallbackQuery.answer(
            "Getting mongodb stats..."
        )
        try:
            pymongo = MongoClient(MONGO_DB_URI)
        except Exception as e:
            print(e)
            return await CallbackQuery.edit_message_text("**Failed to get mongodb stats...**", reply_markup=stats_b)
        try:
            db = pymongo.Sarcastic
        except Exception as e:
            print(e)
            return await CallbackQuery.edit_message_text("**Failed to get mongodb stats...**", reply_markup=stats_b)
        call = db.command("dbstats")
        database = call["db"]
        datasize = call["dataSize"] / 1024
        datasize = str(datasize)
        storage = call["storageSize"] / 1024
        objects = call["objects"]
        collections = call["collections"]
        status = db.command("serverStatus")
        query = status["opcounters"]["query"]
        mver = status["version"]
        mongouptime = status["uptime"] / 86400
        mongouptime = str(mongouptime)
        provider = status["repl"]["tags"]["provider"]
        smex = f"""
➻ <u>**{BOT_NAME} MONGO-DB stats ✨ :**</u>

**Uptime :** {mongouptime[:4]} days
**Version :** {mver}
**Database :** {database}
**Provider :** {provider}
**DB-size :** {datasize[:6]} ᴍʙ
**DB-storage :** {storage} ᴍʙ
**Collections :** {collections}
**Keys :** {objects}
**Queries :** `{query}`"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats_b)
    if command == "get_back":
        smex = f"**Choose an option for getting {BOT_NAME} general stats or assistant stats or overall stats.**"
        await CallbackQuery.edit_message_text(smex, reply_markup=stats_f)
