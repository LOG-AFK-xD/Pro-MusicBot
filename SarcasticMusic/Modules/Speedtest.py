import asyncio
import speedtest

from pyrogram import filters
from SarcasticMusic import app, SUDO_USERS


__MODULE__ = "Speed-test"
__HELP__ = """

/speedtest 
» Check the server's speed, latecy and ping.

(✿◠‿◠)
"""


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("**⇆ Running speedtest .....**")
        test.download()
        m = m.edit("**⇆ Running uploading speedtest...**")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("**↻ Sharing speedtest result...**")
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(filters.command(["speedtest", "sptest", "spt"]) & filters.user(SUDO_USERS))
async def speedtest_function(client, message):
    m = await message.reply_text("**» Running speedtest...**")
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""✯ **Speedtest result** ✯
    
<u>**❥͜͡Ciient :**</u>
**» Isp :** {result['client']['isp']}
**» Country :** {result['client']['country']}
  
<u>**❥͜͡Server :**</u>
**» Name :** {result['server']['name']}
**» Country :** {result['server']['country']}, {result['server']['cc']}
**» Sponsor :** {result['server']['sponsor']}
**» Latecy :** {result['server']['latency']}  
**» Ping :** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, 
        photo=result["share"], 
        caption=output
    )
    await m.delete()
