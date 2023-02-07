from pyrogram import Client, filters
from pyrogram.types import Message

from SarcasticMusic import app
from SarcasticMusic.Cache.admins import AdminActual
from SarcasticMusic.Helpers.Changers import int_to_alpha
from SarcasticMusic.Helpers.Database import (_get_authusers, delete_authuser, get_authuser,
                            get_authuser_count, get_authuser_names,
                            save_authuser)


__MODULE__ = "Auth-user"
__HELP__ = """

**Note :**
• Authorised user can skip, stop and pause stream without admin rights .


/auth [username or reply to a user] 
» add the user to authorized user list of group.

/unauth [username or reply to a user] 
» removes the user from authorized list of group.

/authusers 
» shows the list of authorized user of group.

(✿◠‿◠)
"""


@app.on_message(filters.command("auth") & filters.group)
@AdminActual
async def auth(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**» Reply to a user message or give his/her username 😅.**"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        user_id = message.from_user.id
        token = await int_to_alpha(user.id)
        from_user_name = message.from_user.first_name
        from_user_id = message.from_user.id
        _check = await get_authuser_names(message.chat.id)
        count = 0
        for smex in _check:
            count += 1
        if int(count) == 15:
            return await message.reply_text(
                "**» You can only add 15 user to group auth list 🤷‍♂️**"
            )
        if token not in _check:
            assis = {
                "auth_user_id": user.id,
                "auth_name": user.first_name,
                "admin_id": from_user_id,
                "admin_name": from_user_name,
            }
            await save_authuser(message.chat.id, token, assis)
            await message.reply_text(
                f"**» Sucessfully added {user.first_name} to authorised user list of group (✿◠‿◠)**"
            )
            return
        else:
            await message.reply_text(f"**» {user.first_name} is already clan lover (✿◠‿◠)**")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    token = await int_to_alpha(user_id)
    from_user_name = message.from_user.first_name
    _check = await get_authuser_names(message.chat.id)
    count = 0
    for smex in _check:
        count += 1
    if int(count) == 15:
        return await message.reply_text(
            "**»You can only add 15 user in group auth list (•_•).**"
        )
    if token not in _check:
        assis = {
            "auth_user_id": user_id,
            "auth_name": user_name,
            "admin_id": from_user_id,
            "admin_name": from_user_name,
        }
        await save_authuser(message.chat.id, token, assis)
        await message.reply_text(
            f"**» Sucessfully added {user_name} to authorised users list (✿◠‿◠).**"
        )
        return
    else:
        await message.reply_text(f"**» {user_name} si already clan lover (✿◠‿◠)**")


@app.on_message(filters.command("unauth") & filters.group)
@AdminActual
async def unauth_fe(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**» Reply to a user or give me username of the user 😅**"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        token = await int_to_alpha(user.id)
        deleted = await delete_authuser(message.chat.id, token)
        if deleted:
            return await message.reply_text(
                f"**» Removed {user.first_name} from authorised user list of the group 🙂.**"
            )
        else:
            return await message.reply_text("**» Not in authorised list 🙂**")
    user_id = message.reply_to_message.from_user.id
    token = await int_to_alpha(user_id)
    deleted = await delete_authuser(message.chat.id, token)
    if deleted:
        return await message.reply_text(
            f"**» Removed {message.reply_to_message.from_user.first_name} from authorised user list of group 🙂🥀.**"
        )
    else:
        return await message.reply_text("**» Not in authorised list (¬‿¬)**")


@app.on_message(filters.command("authusers") & filters.group)
async def authusers(_, message: Message):
    _playlist = await get_authuser_names(message.chat.id)
    if not _playlist:
        return await message.reply_text(
            "**» No authorised user fount in group.. how so rude yaar 🙂😂**"
        )
    else:
        j = 0
        m = await message.reply_text(
            "**» Getting authorised user list from mongodb...**"
        )
        msg = "**🥀 Authorised user list :**\n\n"
        for note in _playlist:
            _note = await get_authuser(message.chat.id, note)
            user_id = _note["auth_user_id"]
            user_name = _note["auth_name"]
            admin_id = _note["admin_id"]
            admin_name = _note["admin_name"]
            try:
                user = await app.get_users(user_id)
                user = user.first_name
                j += 1
            except Exception:
                continue
            msg += f"{j}➤ {user}[`{user_id}`]\n"
            msg += f"    ┗ Added by: {admin_name}[`{admin_id}`]\n\n"
        await m.edit_text(msg)
