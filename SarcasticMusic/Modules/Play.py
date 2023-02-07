import asyncio
from os import path

from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, Voice
from youtube_search import YoutubeSearch

from SarcasticMusic import (BOT_USERNAME, DURATION_LIMIT_SEC, DURATION_LIMIT,
                   BOT_NAME, app, db_mem)
from SarcasticMusic.Helpers.Url import get_url
from SarcasticMusic.Cache.checker import checker
from SarcasticMusic.Cache.assistant import AssistantAdd
from SarcasticMusic.Cache.permission import PermissionCheck
from SarcasticMusic.Helpers.Thumbnails import thumb_init
from SarcasticMusic.Helpers.PyTgCalls.Converter import convert
from SarcasticMusic.Helpers.PyTgCalls.Downloader import download
from SarcasticMusic.Helpers.Database import add_served_user, add_served_chat
from SarcasticMusic.Helpers.Changers import seconds_to_min, time_to_seconds
from SarcasticMusic.Helpers.Stream import start_stream, start_stream_audio
from SarcasticMusic.Helpers.Ytinfo import (get_yt_info_id, get_yt_info_query, get_yt_info_query_slider)


loop = asyncio.get_event_loop()


@app.on_message(
    filters.command(["play", f"play@{BOT_USERNAME}", "fuck"]) & filters.group
)
@checker
@PermissionCheck
@AssistantAdd
async def play(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    await add_served_chat(message.chat.id)
    if message.chat.id not in db_mem:
        db_mem[message.chat.id] = {}
    if message.sender_chat:
        return await message.reply_text(
            "**» You are anonymous admin.\n\nRevert to user account to use me babes 🙂✨**"
        )
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    url = get_url(message)
    if audio:
        mystic = await message.reply_text(
            "🔎"
        )

        if audio.file_size > 314572800:
            return await mystic.edit_text(
                "**» Audio fils should be less than 300 Mb**"
            )
        duration_min = seconds_to_min(audio.duration)
        duration_sec = audio.duration
        if (audio.duration) > DURATION_LIMIT_SEC:
            return await mystic.edit_text(
                f"**» {BOT_NAME} doesn't allown to play longer than {DURATION_LIMIT_MIN} minutes 😅**"
            )
        file_name = (
            audio.file_unique_id
            + "."
            + (
                (audio.file_name.split(".")[-1])
                if (not isinstance(audio, Voice))
                else "ogg"
            )
        )
        file_name = path.join(path.realpath("downloads"), file_name)
        file = await convert(
            (await message.reply_to_message.download(file_name))
            if (not path.isfile(file_name))
            else file_name,
        )
        return await start_stream_audio(
            message,
            file,
            "smex1",
            "Given Audio Via Telegram",
            duration_min,
            duration_sec,
            mystic,
        )
    elif url:
        mystic = await message.reply_text("🔎")
        if not message.reply_to_message:
            query = message.text.split(None, 1)[1]
        else:
            query = message.reply_to_message.text
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query(query)
        title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
        if duration_sec > DURATION_LIMIT_SEC:
            return await message.reply_text(
                f"**» {BOT_NAME} doesn't allow to play song longer than {DURATION_LIMIT_MIN} minutes.**"
            )
        downloaded_file = await loop.run_in_executor(
            None, download, videoid, mystic, title
        )
        raw_path = await convert(downloaded_file)
        thumb = await thumb_init(videoid)
        await mystic.delete()
    else:
        if len(message.command) < 2:
            await message.reply_photo(
                photo="SarcasticMusic/Utilities/Play.jpeg",
                caption=(
                    "**➻ This is not correct format to play song **\n\n**Example :** /play [song name or you-tube link or reply to a audio file]"
                ),
            )
            return
        mystic = await message.reply_text("🔎")
        query = message.text.split(None, 1)[1]
        (
            title,
            duration_min,
            duration_sec,
            thumb,
            videoid,
        ) = get_yt_info_query(query)
        await mystic.delete()
    title, duration_min, duration_sec, thumbnail = get_yt_info_id(videoid)
    if duration_sec > DURATION_LIMIT_SEC:
        return await message.reply_text(
            f"**» {BOT_NAME} doesn't allow to play song longer than {DURATION_LIMIT} minutes.**"
        )
    mystic = await message.reply_text(
        f"**{BOT_NAME} Downloader**\n\n**Title :** {title}\n\n0% ■■■■■■■■■■■■ 100%"
    )
    downloaded_file = await loop.run_in_executor(
        None, download, videoid, mystic, title
    )
    chat_id = message.chat.id
    user_id = message.from_user.id
    raw_path = await convert(downloaded_file)
    thumb = await thumb_init(videoid)
    if chat_id not in db_mem:
        db_mem[chat_id] = {}
    await start_stream(
        message,
        raw_path,
        videoid,
        thumb,
        title,
        duration_min,
        duration_sec,
        mystic,
    )
