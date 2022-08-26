import json
import asyncio
import logging
import helpers.globals as globals
from helpers.forwarder import ForwardMessage
from helpers.utils import parse_reply_signal_message, not_sent_channels
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, MessageNotModified
from configs import Config
from database.messages_sql import add_reply_message_map, get_message_map, get_reply_message_map


logger = logging.getLogger(__name__)

# Handle edited message


@Client.on_message(filters.chat(Config.SOURCE_CHAT_ID) & filters.text & (filters.reply | filters.edited))
async def handle_reply_message(client: Client, msg: Message):
    try:
        reply_message = parse_reply_signal_message(msg.text)
        if reply_message is None:
            logger.warn("Reply pattern not matched.")
            return

        await asyncio.sleep(5)
        logger.warn("Checking if reply message exist....")
        is_still_exist = await client.get_messages(msg.chat.id, msg.message_id)
        if not is_still_exist.text:
            logger.warn("Message has been removed or does not exist anymore.")
            return

        forward_id = None  # Holds one of sent reply message id for forwarding

        async with globals.lock_section:
            json_reply_sent_ids = {}
            last_sent_ids = None
            if msg.edit_date:
                last_sent_ids = await get_reply_message_map(msg.message_id)
            else:
                last_sent_ids = await get_message_map(msg.reply_to_message.message_id)

            channel_list, json_last_sent_ids = not_sent_channels(last_sent_ids)
            if len(json_last_sent_ids) == 0:
                return  # No source message found

            for channel_id in json_last_sent_ids:
                await asyncio.sleep(2)
                message_id = json_last_sent_ids[channel_id]
                if msg.edit_date:
                    await client.edit_message_text(chat_id=channel_id, message_id=message_id, text=reply_message)
                    continue
                sent = await client.send_message(chat_id=channel_id, text=reply_message, reply_to_message_id=message_id)
                if sent:
                    json_reply_sent_ids[str(channel_id)] = sent.message_id
                    if channel_id == Config.FORWARD_FROM_CHAT_ID:
                        forward_id = sent.message_id

            if len(json_reply_sent_ids) > 0:
                await add_reply_message_map(msg.message_id, json.dumps(json_reply_sent_ids))
            elif msg.edit_date is None:
                logger.warn("Reply ID Not Found.")

        # Forward message if needed
        if Config.FORWARD_TO_CHAT_ID and Config.FORWARD_FROM_CHAT_ID and forward_id:
            await ForwardMessage(client, forward_id)
        else:
            logger.warn("Cannot Forward.", str(Config.FORWARD_FROM_CHAT_ID), str(
                Config.FORWARD_TO_CHAT_ID), str(forward_id))

    except FloodWait as e:
        await asyncio.sleep(e.x)
        await client.send_message(chat_id="me", text=f"#FloodWait: Stopped ContentGenerator for `{e.x}s`!")
        await asyncio.sleep(Config.SLEEP_TIME)
        await handle_reply_message(client, msg)
    except MessageNotModified as e:
        logger.warn(e.MESSAGE)
    except Exception as err:
        await client.send_message(chat_id="me", text=f"#Error: `{err}`\n\nUnable to Send Message to `{str(Config.DESTINATION_CHAT_ID[0])}`")
