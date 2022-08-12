import re
import asyncio
import logging
import helpers.globals as globals
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from configs import Config


logger = logging.getLogger(__name__)

# Handle edited message


@Client.on_message(filters.chat(Config.SOURCE_CHAT_ID) & filters.text & (filters.reply | filters.edited))
async def handle_edited_message(client: Client, msg: Message):
    try:
        reply_match = re.search(Config.REPLY_MESSAGE_PATTERN, msg.text)
        if reply_match:
            new_message = reply_match.group(1)
        else:
            logger.warn("Reply pattern failed.")
            return

        if msg.edit_date:
            if msg.message_id in globals.edited_message_map.keys():
                msg_id = globals.edited_message_map[msg.message_id]
            if msg_id:
                await client.edit_message_text(chat_id=Config.DESTINATION_CHAT_ID[0], message_id=msg_id, text=msg.text)
        else:
            if msg.reply_to_message.message_id in globals.messages_map_id.keys():
                msg_id = globals.messages_map_id[msg.reply_to_message.message_id]
            if msg_id:
                sent = await client.send_message(chat_id=Config.DESTINATION_CHAT_ID[0], text=new_message, reply_to_message_id=msg_id)
                if sent:
                    globals.edited_message_map[msg.message_id] = sent.message_id
            else:
                logger.warn("Reply ID Not Found.")

    except FloodWait as e:
        await asyncio.sleep(e.x)
        await client.send_message(chat_id="me", text=f"#FloodWait: Stopped ContentGenerator for `{e.x}s`!")
        await asyncio.sleep(Config.SLEEP_TIME)
        await handle_edited_message(client, msg)
    except Exception as err:
        await client.send_message(chat_id="me", text=f"#Error: `{err}`\n\nUnable to Send Message to `{str(Config.DESTINATION_CHAT_ID[0])}`")
