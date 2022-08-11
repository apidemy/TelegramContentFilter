
import re
import asyncio
import logging
from hashlib import sha1
from configs import Config
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from database.messages_sql import add_message_map

logger = logging.getLogger(__name__)

current_hashes = []


@Client.on_message(filters.chat(Config.SOURCE_CHAT_ID) & filters.text & ~filters.edited)
async def handle_new_message(client: Client, msg: Message):
    try:
        # match variable contains a Match object.
        signal_match = re.search(Config.NEW_MESSAGE_PATTERN, msg.text)
        if signal_match:
            ## --- Check 5 --- ##
            targets_pattern = '(Target\s\d\s-\s\d+\.?\d*)'
            targets = re.findall(targets_pattern, msg.text)
            if len(targets) == 0:
                return  # No targets found
            direction_symbol = " 🟢" if signal_match.group(
                2) == "LONG" else " 🔴"
            leverage = signal_match.group(3)
            new_message = "💸📡Futures Scalping📡💸\n\n"\
                "Coin : " + signal_match.group(1) + \
                "\nDirection : " + signal_match.group(2) + direction_symbol + \
                "\n" + leverage + \
                "\n" + signal_match.group(4) + \
                "\n\n" + signal_match.group(5) + \
                "\n\n SCALPING " \
                "\n" + targets[0] + \
                "\n" + targets[1] + \
                "\n" + targets[2] + \
                "\n⚠️ DAY TRADING ⚠️" \
                "\n" + targets[3] + \
                "\n" + targets[4] + \
                "\n" + targets[5] + \
                "\n⚠️⚠️ SWING TRADING ⚠️⚠️" \
                "\n" + targets[6] + \
                "\n" + targets[7]
        else:
            logger.warn("Not a related message.")
            return

        # Check if we added this message recently
        msg_hash = sha1(new_message.encode("utf-8")).hexdigest()
        if msg_hash in current_hashes:
            logger.warn("Already added.")
            return

        current_hashes.append(msg_hash)
        sent = await client.send_message(chat_id=Config.DESTINATION_CHAT_ID[0], text=new_message)
        if sent:
            await add_message_map(msg.message_id, sent.message_id)
            current_hashes.remove(msg_hash)
            logger.warn("Message Sent.")
    except FloodWait as e:
        await asyncio.sleep(e.x)
        await client.send_message(chat_id="me", text=f"#FloodWait: Stopped ContentGenerator for `{e.x}s`!")
        await asyncio.sleep(Config.SLEEP_TIME)
        await handle_new_message(client, msg)
    except Exception as err:
        await client.send_message(chat_id="me", text=f"#Error: `{err}`\n\nUnable to Send Message to `{str(Config.DESTINATION_CHAT_ID[0])}`")
