from Data import Data
import helpers.globals as globals
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup


# Help Message
@Client.on_message(filters.incoming & filters.private & filters.command("help"))
async def help(bot, msg):
    # message_ids = "Message ID maps:\n"

    # for key, value in globals.messages_map_id.items():
    #     message_ids +=

    await bot.send_message(
        msg.chat.id,
        "**Here's how to use me **\n" + Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )
