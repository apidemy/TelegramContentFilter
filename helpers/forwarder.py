from asyncio import sleep
import logging
from random import randint
from re import search
from configs import Config
from pyrogram import Client
from pyrogram.errors import FloodWait

logger = logging.getLogger(__name__)

"""Watch for specific messages using a pattern and forward to specific channel"""


async def ForwardMessage(client: Client, message_id):
    try:
        if Config.FORWARD_TO_CHAT_ID is None or Config.FORWARD_FROM_CHAT_ID is None:
            return

        logger.warn("Check forwarding.")
        could_forward_pattern = "(?s).*Profit:\s\d+\.?\d*(?s).*"

        is_exist = await client.get_messages(Config.FORWARD_FROM_CHAT_ID, message_id)
        if not is_exist.text or not search(could_forward_pattern, is_exist.text):
            logger.warn("No message found for forwarding.")
            return

        # Set a delay
        await sleep(randint(10, 30))
        sent = await client.forward_messages(chat_id=Config.FORWARD_TO_CHAT_ID, from_chat_id=Config.FORWARD_FROM_CHAT_ID, message_ids=message_id)
        if sent:
            logger.warn("Message Forwarded.")

    except FloodWait as e:
        await sleep(e.x)
        await client.send_message(chat_id="me", text=f"#FloodWait: Stopped Forwarder for `{e.x}s`!")
        await sleep(Config.SLEEP_TIME)
        await ForwardMessage(client, message_id)
    except Exception as err:
        await client.send_message(chat_id="me", text=f"#ERROR: `{err}`\n\nUnable to Forward Message to `{str(Config.DESTINATION_CHAT_ID)}`")
