import re
import asyncio
import logging
from hashlib import sha1
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from helpers.filters import FilterMessage
from helpers.file_size_checker import CheckFileSize
from helpers.block_exts_handler import CheckBlockedExt
from database.messages_sql import add_edited_message_map, get_edited_message_map, get_message_map, add_message_map, is_message_exist

logger = logging.getLogger(__name__)


async def ContentGenerator(client: Client, msg: Message):
    try:
        ## --- Check 1 --- ##
        can_forward = await FilterMessage(message=msg)
        if can_forward == 400:
            logger.info("FilterMessage not passed.")
            return
        ## --- Check 2 --- ##
        has_blocked_ext = await CheckBlockedExt(event=msg)
        if has_blocked_ext is True:
            logger.info("CheckBlockedExt not passed.")
            return
        ## --- Check 3 --- ##
        file_size_passed = await CheckFileSize(msg=msg)
        if file_size_passed is False:
            logger.info("CheckFileSize not passed.")
            return
        is_reply_message = False
        ## --- Check 4 --- ##
        signal_pattern = '(?s).*\.\.\.\s([A-Za-z0-9]+)\s\.\.\.(?s).*𝓓𝓲𝓻𝓮𝓬𝓽𝓲𝓸𝓷\s:\s(SHORT|LONG)' \
            '(?s).*(Leverage\s:\s\w+\s\d+x)' \
            '(?s).*(Entry\s:\s\d+\.?\d*\s-\s\d+\.?\d*)' \
            '(?s).*(.Stoploss\s:\s\d+\.?\d*.)'\
            '(?s).*'

        # match variable contains a Match object.
        signal_match = re.search(signal_pattern, msg.text)
        if signal_match:
            ## --- Check 5 --- ##
            targets_pattern = '(Target\s\d\s-\s\d+\.?\d*)'
            targets = re.findall(targets_pattern, msg.text)
            if len(targets) == 0:
                return  # No targets found
            direction_symbol = " 🟢" if signal_match.group(
                2) == "LONG" else " 🔴"
            leverage = signal_match.group(3)
            if "Cross 20x" in leverage:
                leverage = "Leverage : Cross 5x"
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
        elif msg.reply_to_message and msg.reply_to_message.message_id:
            reply_pattern = '([\w\s,]+\\n#[A-Za-z0-9]+/USDT(?s).*)'
            reply_match = re.search(reply_pattern, msg.text)
            if reply_match:
                new_message = reply_match.group(1)
                is_reply_message = True
            else:
                logger.info("Reply pattern failed.")
                return
        else:
            logger.info("Not related message.")
            return

        try:
            if is_reply_message:
                if msg.edit_date:
                    msg_id = await get_edited_message_map(msg.message_id)
                    if msg_id and msg_id[0]:
                        await client.edit_message_text(chat_id=Config.FORWARD_TO_CHAT_ID[0], message_id=msg_id[0], text=msg.text)
                else:
                    msg_id = await get_message_map(msg.reply_to_message.message_id)
                    if msg_id and msg_id[0]:
                        sent = await client.send_message(chat_id=Config.FORWARD_TO_CHAT_ID[0], text=new_message, reply_to_message_id=msg_id[0])
                        if sent:
                            await add_edited_message_map(msg.message_id, sent.message_id)
                    else:
                        logger.info("Reply ID Not Found.")
                return
            # Check if we added this message recently
            msg_hash = sha1(msg.text.encode("utf-8")).hexdigest()
            msg_exist = await is_message_exist(msg_hash)
            if msg_exist:
                logger.info("Already added.")
                return
            sent = await client.send_message(chat_id=Config.FORWARD_TO_CHAT_ID[0], text=new_message)
            if sent:
                await add_message_map(msg.message_id,
                                      sent.message_id,
                                      msg_hash)
                logger.info("Message Sent.")
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await client.send_message(chat_id="me", text=f"#FloodWait: Stopped ContentGenerator for `{e.x}s`!")
            await asyncio.sleep(Config.SLEEP_TIME)
            await ContentGenerator(client, msg)
        except Exception as err:
            await client.send_message(chat_id="me", text=f"#Error: `{err}`\n\nUnable to Send Message to `{str(Config.FORWARD_TO_CHAT_ID[0])}`")
    except Exception as err:
        await client.send_message(chat_id="me", text=f"#ERROR: `{err}`")
