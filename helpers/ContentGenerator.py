import re
import random
import datetime
import asyncio
from configs import Config
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from helpers.filters import FilterMessage
from helpers.file_size_checker import CheckFileSize
from helpers.block_exts_handler import CheckBlockedExt

messages_map_id = {}


async def ContentGenerator(client: Client, msg: Message):
    try:
        ## --- Check 1 --- ##
        time = datetime.datetime.now()
        can_forward = await FilterMessage(message=msg)
        if can_forward == 400:
            print("Info: FilterMessage not passed. " +
                  time.strftime('%Y-%m-%d %H:%M:%S'))
            return 100
        ## --- Check 2 --- ##
        has_blocked_ext = await CheckBlockedExt(event=msg)
        if has_blocked_ext is True:
            print("Info: CheckBlockedExt not passed. " +
                  time.strftime('%Y-%m-%d %H:%M:%S'))
            return 400
        ## --- Check 3 --- ##
        file_size_passed = await CheckFileSize(msg=msg)
        if file_size_passed is False:
            print("Info: CheckFileSize not passed. " +
                  time.strftime('%Y-%m-%d %H:%M:%S'))
            return 400
        # Set a delay
        await asyncio.sleep(random.randint(1, 2))
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
                return 600  # No targets found
            direction_symbol = " 🟢" if signal_match.group(
                2) == "LONG" else " 🔴"
            new_message = "$$$📡Futures Scalping📡$$$\n\n"\
                "Coin : " + signal_match.group(1) + \
                "\nDirection : " + signal_match.group(2) + direction_symbol + \
                "\n" + signal_match.group(3) + \
                "\n" + signal_match.group(4) + \
                "\n\n" + signal_match.group(5) + \
                "\n\n❗️ SCALPING ❗️" \
                "\n" + targets[0] + \
                "\n" + targets[1] + \
                "\n" + targets[2] + \
                "\n❗️ DAY TRADING ❗️" \
                "\n" + targets[3] + \
                "\n" + targets[4] + \
                "\n" + targets[5] + \
                "\n❗️ SWING TRADING ❗️" \
                "\n" + targets[6] + \
                "\n" + targets[7]
        elif msg.reply_to_message and msg.reply_to_message.message_id:
            reply_pattern = '([\w\s,]+\\n#[A-Za-z0-9]+/USDT(?s).*)'
            reply_match = re.search(reply_pattern, msg.text)
            if reply_match:
                new_message = reply_match.group(1)
                is_reply_message = True
            else:
                print("Info: Reply pattern failed. " +
                      time.strftime('%Y-%m-%d %H:%M:%S'))
                return 400
        else:
            print("Info: Not related message. " +
                  time.strftime('%Y-%m-%d %H:%M:%S'))
            return 400

        for i in range(len(Config.FORWARD_TO_CHAT_ID)):
            try:
                if is_reply_message:
                    if msg.reply_to_message.message_id in messages_map_id.keys():
                        msg_id = messages_map_id[msg.reply_to_message.message_id]
                        await client.send_message(chat_id=Config.FORWARD_TO_CHAT_ID[i], text=new_message, reply_to_message_id=msg_id)
                    else:
                        print("Info: Reply ID Not Found. " +
                              time.strftime('%Y-%m-%d %H:%M:%S'))
                    return 700
                sent = await client.send_message(chat_id=Config.FORWARD_TO_CHAT_ID[i], text=new_message)
                if sent:
                    messages_map_id[msg.message_id] = sent.message_id
                    print("Info: Message Sent. " +
                          time.strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    print("Info: Message Not Sent. " +
                          time.strftime('%Y-%m-%d %H:%M:%S'))
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await client.send_message(chat_id="me", text=f"#FloodWait: Stopped Forwarder for `{e.x}s`!")
                await asyncio.sleep(Config.SLEEP_TIME)
                await ContentGenerator(client, msg)
            except Exception as err:
                await client.send_message(chat_id="me", text=f"#Error: `{err}`\n\nUnable to Forward Message to `{str(Config.FORWARD_TO_CHAT_ID[i])}`")
    except Exception as err:
        await client.send_message(chat_id="me", text=f"#ERROR: `{err}`")
