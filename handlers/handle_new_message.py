import json
import asyncio
import logging
from configs import Config
import helpers.globals as globals
from helpers.utils import parse_signal_message, not_sent_channels
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from database.messages_sql import add_message_map, get_message_map, update_message_map

logger = logging.getLogger(__name__)


@Client.on_message(filters.chat(Config.SOURCE_CHAT_ID) & filters.text & ~filters.edited & ~filters.reply)
async def handle_new_message(client: Client, msg: Message):
    try:
        # match variable contains a Match object.
        new_message = parse_signal_message(msg.text)
        if new_message is None:
            logger.warn("Not a related message.")
            return

        await asyncio.sleep(5)
        logger.warn("Checking if exist....")
        is_still_exist = await client.get_messages(msg.chat.id, msg.message_id)
        if not is_still_exist.text:
            logger.warn("Message has been removed or does not exist anymore.")
            return

        async with globals.lock_section:
            last_sent_ids = await get_message_map(msg.message_id)
            channel_list, json_last_sent_ids = not_sent_channels(last_sent_ids)
            is_update = len(json_last_sent_ids) > 0
            for channel_id in channel_list:
                sent = await client.send_message(chat_id=channel_id, text=new_message)
                if sent:
                    json_last_sent_ids[str(channel_id)] = sent.message_id
                    logger.warn("Message Sent to channel: " + str(channel_id))
                await asyncio.sleep(2)
            if is_update and len(channel_list) > 0:
                await update_message_map(msg.message_id, json.dumps(json_last_sent_ids))
            else:
                await add_message_map(msg.message_id, json.dumps(json_last_sent_ids))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await client.send_message(chat_id="me", text=f"#FloodWait: Stopped ContentGenerator for `{e.x}s`!")
        await asyncio.sleep(Config.SLEEP_TIME)
        await handle_new_message(client, msg)
    except Exception as err:
        await client.send_message(chat_id="me", text=f"#Error: `{err}`\n\nUnable to Send Message to `{str(Config.DESTINATION_CHAT_ID[0])}`")
