from pyrogram.types import InlineKeyboardButton


class Data:
    # Start Message
    START = """
Hello {}

Welcome to {}

If you don't trust this bot,
1) don't read this message

This Bot Handles contents of a channel.Thank you By @ScalpFutures
    """

    # Home Button
    home_buttons = [
        [InlineKeyboardButton(text="🏠 Home 🏠", callback_data="home")]
    ]

    # Rest Buttons
    buttons = [
        [InlineKeyboardButton("🔥 Check Bot Status 🔥",
                              callback_data="status")],
        [InlineKeyboardButton("✨ Maintaned By ✨",
                              url="https://t.me/ScalpFutures")],
        [
            InlineKeyboardButton("How to use me❔", callback_data="help"),
            InlineKeyboardButton("🎪 About 🎪", callback_data="about")
        ],
    ]

    # Help Message
    HELP = """
✨ **Available Commands** ✨

/about - About this bot
/help - How to use this bot
/start - Start Bot
/generate - Start Generating Session
/cancel - Cancel process
/restart - Restart process
"""

    # About Message
    ABOUT = """
**About This Bot** 

A telegram bot to handle channel messages

Developer : @ScalpFutures
    """
