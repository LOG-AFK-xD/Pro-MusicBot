import re
import os

import lyricsgenius
from pyrogram import filters
from pyrogram.types import Message
from youtubesearchpython import VideosSearch

from SarcasticMusic import BOT_NAME, app


__MODULE__ = "Lyrics"
__HELP__ = """

/lyrics [song]
» shows the lyrics of the seached song.

(✿◠‿◠)
"""


@app.on_message(filters.command(["lyrics", "lyric"]))
async def lrsearch(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**Example :**\n\n/lyrics [Love dose]")
    m = await message.reply_text("🔎")
    query = message.text.split(None, 1)[1]
    x = "OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI"
    y = lyricsgenius.Genius(x)
    y.verbose = False
    S = y.search_song(query, get_full_info=False)
    if S is None:
        return await m.edit("**» Lyrics not fount for this song, tune hi galat likha hoga padta toh tu hai nahi 🙂😂**")
    xxx = f"""
**Lyrics powered by {BOT_NAME}**

**Searched :-** __{query}__
**Title :-** __{S.title}__
**Artist :-** {S.artist}

**Lyrics :**

{S.lyrics}"""
    if len(xxx) > 4096:
        await m.delete()
        filename = "Sarcastic-lyrics.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(xxx.strip()))
        await message.reply_document(
            document=filename,
            caption=f"**OUTPUT:**\n\n`Lyrics`",
            quote=False,
        )
        os.remove(filename)
    else:
        await m.edit(xxx)

