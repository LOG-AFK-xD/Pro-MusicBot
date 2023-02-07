import config

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery, Message

from SarcasticMusic import app, SUDO_USERS
from SarcasticMusic.Helpers import Help
from SarcasticMusic.Helpers.Inline import help_panel, help_markup



@app.on_callback_query(filters.regex("sarcastic_help"))
async def help_menu(_, CallbackQuery):
    await CallbackQuery.message.edit(
       text=f"""Hey {CallbackQuery.from_user.first_name},

All of my command are listed below in the button given below, click on it and get the info and help 🥀.

All of my command can be used with : `/`

(✿◡‿◡)
""",
       reply_markup=help_panel)


@app.on_callback_query(filters.regex("help_callback"))
async def helper_cb(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    if cb == "ADMIN":
        await CallbackQuery.edit_message_text(
            Help.ADMIN, reply_markup=help_markup
        )
    elif cb == "AUTH":
        await CallbackQuery.edit_message_text(
            Help.AUTH, reply_markup=help_markup
        )
    elif cb == "PLAY":
        await CallbackQuery.edit_message_text(
            Help.PLAY, reply_markup=help_markup
        )
    elif cb == "OWNER":
        await CallbackQuery.edit_message_text(
            Help.OWNER, reply_markup=help_markup
        )
    elif cb == "SUDO":
        await CallbackQuery.edit_message_text(
            Help.SUDO, reply_markup=help_markup
        )
    elif cb == "TOOLS":
        await CallbackQuery.edit_message_text(
            Help.TOOLS, reply_markup=help_markup
        )
