from Data import Data
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup


# Help Message
@Client.on_message(filters.incoming & filters.private & filters.command("help"))
async def help(bot, msg):
    await bot.send_message(
        msg.chat.id,
        "**Here's how to use me **\n" + Data.HELP,
        reply_markup=InlineKeyboardMarkup(Data.home_buttons)
    )
