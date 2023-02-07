import config

from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)
from SarcasticMusic import BOT_USERNAME, F_OWNER


def start_pannel():
        buttons = [
            [
                InlineKeyboardButton(
                    text="+ Add me to your clan +", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❄ Help ❄", callback_data="sarcastic_help"
                ),
                InlineKeyboardButton(
                    text="💡 Owner 💡", user_id=F_OWNER
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ Support ✨", url=config.SUPPORT_CHAT
                ),
                InlineKeyboardButton(
                    text="🍕 Updates 🍕", url=config.SUPPORT_CHANNEL
                ),
            ],
        ]
        return buttons


def private_panel():
        buttons = [
            [
                InlineKeyboardButton(
                    text="+ Add me to your clan +", url=f"https://t.me/{BOT_USERNAME}?startgroup=true"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❄ Help ❄", callback_data="sarcastic_help"
                ),
                InlineKeyboardButton(
                    text="💡 Owner 💡", user_id=F_OWNER
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ Support ✨", url=config.SUPPORT_CHAT
                ),
                InlineKeyboardButton(
                    text="🍕 Updates 🍕", url=config.SUPPORT_CHANNEL
                ),
            ],
        ]
        return buttons
