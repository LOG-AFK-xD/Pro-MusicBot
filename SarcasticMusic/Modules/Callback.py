import os
import asyncio
import random

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery
from asyncio import QueueEmpty
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream

from config import get_queue
from SarcasticMusic.Cache.checker import checkerCB
from SarcasticMusic.Cache.admins import AdminRightsCheck, AdminRightsCheckCB
from SarcasticMusic.Helpers.Thumbnails import thumb_init
from SarcasticMusic.Helpers.Ytinfo import get_yt_info_id
from SarcasticMusic.Helpers.PyTgCalls import Queues, Sarcastic
from SarcasticMusic.Helpers.Changers import time_to_seconds
from SarcasticMusic.Helpers.PyTgCalls.Converter import convert
from SarcasticMusic.Helpers.PyTgCalls.Downloader import download
from SarcasticMusic import BOT_USERNAME, BOT_NAME, app, db_mem
from SarcasticMusic.Helpers.Inline import (audio_markup, primary_markup, close_key)
from SarcasticMusic.Helpers.Database import (add_active_chat, is_active_chat, remove_active_chat, is_music_playing, music_off, music_on)


loop = asyncio.get_event_loop()


@app.on_callback_query(
    filters.regex(pattern=r"^(pausecb|skipcb|stopcb|resumecb)$")
)
@AdminRightsCheckCB
@checkerCB
async def admin_risghts(_, CallbackQuery):
    global get_queue
    command = CallbackQuery.matches[0].group(1)
    if not await is_active_chat(CallbackQuery.message.chat.id):
        return await CallbackQuery.answer(
            "» Did you remember that you have played something ?", show_alert=True
        )
    chat_id = CallbackQuery.message.chat.id
    if command == "pausecb":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer(
                "» Stream already paused.", show_alert=True
            )
        await music_off(chat_id)
        await Sarcastic.pytgcalls.pause_stream(chat_id)
        await CallbackQuery.message.reply_text(
            f"➻ **Stream paused** ☁️\n│ \n└By : {CallbackQuery.from_user.first_name} 🥀",
            reply_markup=audio_markup,
        )
        await CallbackQuery.answer("» Stream paused 😅.")
    if command == "resumecb":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer(
                "» Did you remembered that you have played something ?", show_alert=True
            )
        await music_on(chat_id)
        await Sarcastic.pytgcalls.resume_stream(chat_id)
        await CallbackQuery.message.reply_text(
            f"➻ **Stream resumed** ✨\n│ \n└By : {CallbackQuery.from_user.first_name} 🥀",
            reply_markup=audio_markup,
        )
        await CallbackQuery.answer("» Stream resumed 😁.")
    if command == "stopcb":
        try:
            Queues.clear(chat_id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await Sarcastic.pytgcalls.leave_group_call(chat_id)
        await CallbackQuery.message.reply_text(
            f"➻ **Stream ended/stopped** ❄\n│ \n└By : {CallbackQuery.from_user.first_name} 🥀",
            reply_markup=close_key,
        )
        await CallbackQuery.message.delete()
        await CallbackQuery.answer("» Stream ended.")
    if command == "skipcb":
        Queues.task_done(chat_id)
        if Queues.is_empty(chat_id):
            await remove_active_chat(chat_id)
            await CallbackQuery.message.reply_text(
                f"➻ **Stream skipped** 🙂\n│ \n└By : {CallbackQuery.from_user.first_name} 🥀\n\n» No more track in playlist of {CallbackQuery.message.chat.title}, **Leaving voice-chat.**",
              reply_markup=close_key,
            )
            await Sarcastic.pytgcalls.leave_group_call(chat_id)
            await CallbackQuery.message.delete()
            await CallbackQuery.answer(
                "» Skipped no more track in playlist 😅"
            )
            return
        else:
            videoid = Queues.get(chat_id)["file"]
            got_queue = get_queue.get(CallbackQuery.message.chat.id)
            if got_queue:
                got_queue.pop(0)
            finxx = f"{videoid[0]}{videoid[1]}{videoid[2]}"
            aud = 0
            if str(finxx) != "raw":
                await CallbackQuery.message.delete()
                await CallbackQuery.answer(
                    "Stream skipped..."
                )
                mystic = await CallbackQuery.message.reply_text(
                    f"**Downloading next track from playlist...\n\nstream skipped by {CallbackQuery.from_user.mention} !**🥀"
                )
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                ) = get_yt_info_id(videoid)
                await mystic.edit(
                    f"**{BOT_NAME} Downloader**\n\n**Title :** {title[:40]}\n\n0% ■■■■■■■■■■■■ 100%"
                )
                downloaded_file = await loop.run_in_executor(
                    None, download, videoid, mystic, title
                )
                raw_path = await convert(downloaded_file)
                await Sarcastic.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            raw_path,
                        ),
                    ),
                )
                chat_title = CallbackQuery.message.chat.title
                thumb = await thumb_init(videoid)
                buttons = primary_markup(
                    videoid,
                    CallbackQuery.from_user.id
                )
                await mystic.delete()
                mention = db_mem[videoid]["username"]
                final_output = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=(
                        f"<b>➻ Started streaming</b>\n\n<b>✨ Title :</b> [{title[:40]}](https://www.youtube.com/watch?v={videoid})\n☁ <b>Duration :</b> {duration_min} minutes\n🥀 <b>Requested by :</b> {mention}"
                    ),
                )
                os.remove(thumb)

            else:
                await CallbackQuery.message.delete()
                await CallbackQuery.answer("Stream skipped...")
                await Sarcastic.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            videoid,
                        ),
                    ),
                )
                afk = videoid
                title = db_mem[videoid]["title"]
                duration_min = db_mem[videoid]["duration"]
                duration_sec = int(time_to_seconds(duration_min))
                mention = db_mem[videoid]["username"]
                videoid = db_mem[videoid]["videoid"]
                if str(videoid) == "smex1":
                    buttons = primary_markup(
                        videoid,
                        CallbackQuery.from_user.id,
                    )
                    thumb = "SarcasticMusic/Utilities/Audio.jpeg"
                    aud = 1
                else:
                    _path_ = _path_ = (
                        (str(afk))
                        .replace("_", "", 1)
                        .replace("/", "", 1)
                        .replace(".", "", 1)
                    )
                    thumb = f"SarcasticMusic/Cache/{_path_}final.png"
                    buttons = primary_markup(
                        videoid,
                        CallbackQuery.from_user.id,
                    )
                final_output = await CallbackQuery.message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"<b>➻ Started streaming</b>\n\n<b>✨ Title :</b> {title[:40]}\n☁ <b>Duration :</b> {duration_min} minutes\n🥀 <b>Requested by :</b> {mention}",
                )


@app.on_callback_query(filters.regex("close"))
async def closed(_, query: CallbackQuery):
    await query.message.delete()
    await query.answer()

