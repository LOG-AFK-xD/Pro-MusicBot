from SarcasticMusic import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


help_panel = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Admins",
                    callback_data="help_callback ADMIN",
                ),
                InlineKeyboardButton(
                    text="Auth",
                    callback_data="help_callback AUTH",
                ),
                InlineKeyboardButton(
                    text="Play",
                    callback_data="help_callback PLAY",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="Owner",
                    callback_data="help_callback OWNER",
                ),
                InlineKeyboardButton(
                    text="Sudo",
                    callback_data="help_callback SUDO",
                ),
                InlineKeyboardButton(
                    text="Tools",
                    callback_data="help_callback TOOLS",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="↬ Back ↫",
                    callback_data=f"sarcastic_home",
                ),
                InlineKeyboardButton(
                    text="↬ Close ↫",
                    callback_data=f"close"
                ),
            ]
        ]
    )


help_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="↬ Back ↫",
                    callback_data=f"sarcastic_help",
                ),
                InlineKeyboardButton(
                    text="↬ Close ↫",
                    callback_data=f"close"
                )
            ]
        ]
    )
