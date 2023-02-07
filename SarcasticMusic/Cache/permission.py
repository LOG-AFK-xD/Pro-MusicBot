from typing import Dict, List, Union

from SarcasticMusic import BOT_ID, app


def PermissionCheck(mystic):
    async def wrapper(_, message):
        a = await app.get_chat_member(message.chat.id, BOT_ID)
        if a.status != "administrator":
            return await message.reply_text(
                "» Please give me below permission :\n\n"
                + "\n• **Delete messages**"
                + "\n• **Manage video-chats**"
                + "\n• **Invite user via links.**"
            )
        if not a.can_manage_voice_chats:
            await message.reply_text(
                "» I don't have permission to :"
                + "\n\n**manage video-chats ≡(▔﹏▔)≡**"
            )
            return
        if not a.can_delete_messages:
            await message.reply_text(
                "» I don't have permission to :"
                + "\n\n**delete messages ＞︿＜**"
            )
            return
        if not a.can_invite_users:
            await message.reply_text(
                "» I don't have permission to :"
                + "\n\n**invite user via link （＞人＜；）**"
            )
            return
        return await mystic(_, message)

    return wrapper
