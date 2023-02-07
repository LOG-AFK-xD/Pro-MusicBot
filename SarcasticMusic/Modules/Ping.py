import os
import time
import config
from datetime import datetime

import psutil
from pyrogram import filters
from pyrogram.types import Message

from SarcasticMusic.Helpers.Inline import ping_ig
from SarcasticMusic.Helpers.Ping import get_readable_time
from SarcasticMusic import BOT_USERNAME, BOT_NAME, app, StartTime


__MODULE__ = "Ping"
__HELP__ = """

/ping or /alive
» check the bot is alive or fucked 

(✿◠‿◠)
"""


async def sarcastic_ping():
    uptime = int(time.time() - StartTime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    sarcastic = f"""
✨ Uptime : {get_readable_time((uptime))}
☁ Cpu : {cpu}%
❄ Ram : {mem}%
💠 Disk : {disk}%"""
    return sarcastic

@app.on_message(filters.command(["ping", "alive", f"ping@{BOT_USERNAME}"]))
async def ping(_, message):
    hmm = await message.reply_photo(
        photo=config.PING_IMG,
        caption="**» Pinging pong my babu...**",
    )
    hehe = await sarcastic_ping()
    start = datetime.now()
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    await hmm.edit_text(
        f"**» Pong baby !**\n`☁ {resp}`ms\n\n<b><u>{BOT_NAME} system stats :</u></b>{hehe}",
        reply_markup=ping_ig,
    )
