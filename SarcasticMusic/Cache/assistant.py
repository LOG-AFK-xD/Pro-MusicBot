from typing import Dict, List, Union

from pyrogram import filters
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from SarcasticMusic import (ASSID, ASSMENTION, ASSNAME, ASSUSERNAME, BOT_ID, BOT_NAME, app, Ass)



@app.on_callback_query(filters.regex("unban_assistant"))
async def unban_assistant_(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    a = await app.get_chat_member(CallbackQuery.message.chat.id, BOT_ID)
    if not a.can_restrict_members:
        return await CallbackQuery.answer(
            "» Wth..! I don't have right to ban or unban user in this chat",
            show_alert=True,
        )
    else:
        try:
            await app.unban_chat_member(
                CallbackQuery.message.chat.id, user_id
            )
        except:
            return await CallbackQuery.answer(
                "» Failed to unban assistant",
                show_alert=True,
            )
        return await CallbackQuery.edit_message_text(
            "» Assistant sucessfully unbanned now you can play the song again."
        )

def AssistantAdd(mystic):
    async def wrapper(_, message):
        try:
            b = await app.get_chat_member(message.chat.id, ASSID)
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="• Click here •",
                            callback_data=f"unban_assistant a|{ASSID}",
                        )
                    ],
                ]
            )
            if b.status == "kicked":
                return await message.reply_text(
                    f"» {BOT_NAME} assistant is banned in this chat.\n\nAssistant id : `{ASSID}`\nAssistant user-name : @{ASSUSERNAME}\n\nClick on the button given below to unban the assistant.",
                    reply_markup=key,
                )
            elif b.status == "banned":
                return await message.reply_text(
                    f"» {BOT_NAME} assistant is banned in this cha.\n\nAssistant id : `{ASSID}`\nAssistant user-name : @{ASSUSERNAME}\n\nClick on the button given below to unban the assistant.",
                    reply_markup=key,
                )
        except UserNotParticipant:
            if message.chat.username:
                try:
                    await Ass.join_chat(message.chat.username)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    await message.reply_text(
                        f"» {BOT_NAME} assistant failed to join the chat.\n\n**Reason** : {e}"
                    )
                    return
            else:
                try:
                    invitelink = await app.export_chat_invite_link(
                        message.chat.id
                    )
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace(
                            "https://t.me/+", "https://t.me/joinchat/"
                        )
                    await Ass.join_chat(invitelink)
                    await message.reply(
                        f"» {BOT_NAME} Assistant sucessfully joined the chat.\n\n• Ass id : `{ASSID}` \n• Ass name : {ASSNAME}\n• Ass username : @{ASSUSERNAME}",
                    )
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    await message.reply_text(
                        f"» {BOT_NAME} Assistant failed to join the chat.\n\n**Reason** : {e}"
                    )
                    return
        return await mystic(_, message)

    return wrapper
