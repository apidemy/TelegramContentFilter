import os
import sys
import time
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config
from helpers.kanger import Kanger
from helpers.content_generator import ContentGenerator
# from helpers.forwarder import ForwardMessage
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood

User = Client(session_name=Config.STRING_SESSION,
              api_hash=Config.API_HASH, api_id=Config.API_ID)


@User.on_message(filters.text | filters.media)
async def main(client: Client, message: Message):
    if (-100 in Config.FORWARD_TO_CHAT_ID) or (-100 in Config.FORWARD_FROM_CHAT_ID):
        try:
            await client.send_message(chat_id="me",
                                      text=f"#VARS_MISSING: Please Set `FORWARD_FROM_CHAT_ID` or `FORWARD_TO_CHAT_ID` Config!")
        except FloodWait as e:
            await asyncio.sleep(e.x)
        return
    if (message.text == "!start") and (message.from_user.id == (await client.get_me()).id):
        await message.edit(text=f"Hi, **{(await client.get_me()).first_name}**!\nThis is a Content Filter Userbot.", parse_mode="Markdown",
                           disable_web_page_preview=True)
    elif (message.text == "!help") and (message.from_user.id == (await client.get_me()).id):
        await message.edit(
            text=Config.HELP_TEXT,
            parse_mode="Markdown", disable_web_page_preview=True)
    elif (message.text in ["!restart", "!stop"]) and (message.from_user.id == (await client.get_me()).id):
        if Config.HEROKU_APP is None:
            await message.edit(
                text="Restarting Userbot ...",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            # https://stackoverflow.com/a/57032597/15215201
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:
            await message.edit(
                text="Restarting Heroku Dyno ..."
            )
            Config.HEROKU_APP.restart()
            time.sleep(30)
    elif (message.text == "!kang") and (message.from_user.id == (await client.get_me()).id):
        if len(Config.FORWARD_FROM_CHAT_ID) > 1:
            await message.edit(
                text="Sorry Sir,\nWe can Kang only one Chat! But you put multiple Chat IDs in `FORWARD_FROM_CHAT_ID` Config!",
                disable_web_page_preview=True
            )
            return
        await message.edit(
            text=f"Trying to Get All Messages from `{str(Config.FORWARD_FROM_CHAT_ID[0])}` and Forwarding to {' '.join(str(Config.FORWARD_TO_CHAT_ID))} ...",
            parse_mode="Markdown", disable_web_page_preview=True)
        await asyncio.sleep(5)
        try_kang = await Kanger(c=User, m=message)
        if try_kang == 400:
            return
    elif message.chat.id in Config.FORWARD_FROM_CHAT_ID:
        # Check if the message exist for atleast two seconds
        await ContentGenerator(client, message)

# Run User Bot
if __name__ == "__main__":
    try:
        User.start()
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except:
        print("Exeption: Cannot run app")
        raise
    uname = User.get_me().username
    print(f"@{uname} Started Successfully!")
    idle()
    User.stop()
    print("Bot stopped!")
