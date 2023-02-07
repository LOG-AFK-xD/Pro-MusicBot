import config
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


ping_ig = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="↬ Support ↫",
                    url=config.SUPPORT_CHAT,
                ),
                InlineKeyboardButton(
                    text="↬ Source ↫",
                    url="https://t.me/Redirect_graph/5"
                )
            ]
        ]
    )
