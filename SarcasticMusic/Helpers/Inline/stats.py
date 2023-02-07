import config
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)


stats_f = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="↬ General ↫", callback_data=f"bot_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text="↬ System ↫", callback_data=f"sys_stats"
            ),
            InlineKeyboardButton(
                text="↬ MongoDB ↫", callback_data=f"mongo_stats"
            )
        ],
        [
            InlineKeyboardButton(
                text="✨ Support ✨", url=config.SUPPORT_CHAT
            ),
                        InlineKeyboardButton(
                text="↻ Close ↺", callback_data=f"close"
            )
        ],
    ]
)



stats_b = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Back", callback_data=f"get_back"
            ),
            InlineKeyboardButton(
                text="✨ Support ✨", url=config.SUPPORT_CHAT
            )
        ],
    ]
)

