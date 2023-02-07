import config
from SarcasticMusic import BOT_USERNAME, app
from SarcasticMusic.Helpers.Database import is_gbanned_user, is_on_off


def checker(mystic):
    async def wrapper(_, message):
        if message.sender_chat:
            return await message.reply_text(
                "**» You are an anonymous admin.\n\n• Revert back to user account for using me 🙂**"
            )
        if await is_on_off(1):
            if int(message.chat.id) != int(LOGGER_ID):
                return await message.reply_text(
                    f"» {BOT_NAME} is under maintenance.\n\nIf you wanna know the reason you can ask [HERE]({config.SUPPORT_CHAT}) !",
                    disable_web_page_preview=True,
                )
        if await is_gbanned_user(message.from_user.id):
            return await message.reply_text(
                f"**» Globally banned user «**\n\nAccording to my database you are gbanned by my owner, so you can't use me.\n\nVisit : [Support chat]({config.SUPPORT_CHAT})",
                 disable_web_page_preview=True,
            )
        return await mystic(_, message)

    return wrapper


def checkerCB(mystic):
    async def wrapper(_, CallbackQuery):
        if await is_on_off(1):
            if int(CallbackQuery.message.chat.id) != int(LOGGER_ID):
                return await CallbackQuery.answer(
                    "» {BOT_NAME} is under maintenance.",
                    show_alert=True,
                )
        if await is_gbanned_user(CallbackQuery.from_user.id):
            return await CallbackQuery.answer(
                "» ʙʟᴏᴏᴅʏ ᴍᴏᴛʜᴇʀғᴜ*ᴋᴇʀ\n\nʏᴏᴜ'ʀᴇ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ғʀᴏᴍ ᴛʜɪs ʙᴏᴛ's ᴏᴡɴᴇʀ. sᴏ ᴛʜᴇ ᴏɴʟʏ ᴛʜɪɴɢ ʏᴏᴜ ᴄᴀɴ ᴅᴏ ɪs : ɢᴏ ᴀʜᴇᴀᴅ ᴀɴᴅ ғᴜ*ᴋ ᴏғғ.", show_alert=True
            )
        return await mystic(_, CallbackQuery)

    return wrapper
