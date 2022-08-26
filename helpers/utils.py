# -*- coding: utf-8 -*-

import re
import json
from configs import Config

"""
helpers.util
~~~~~~~~~~~~~~

This module provides utility functions that are useful for
parsing incomming messages and generate your output message structure
using regex or so forth.
"""


def parse_signal_message(message_text):
    """Parse message and look for defined patter and return new structure of current message"""

    new_message = None

    signal_match = re.search(Config.NEW_MESSAGE_PATTERN, message_text)
    if signal_match:
        targets_pattern = '(Target\s\d\s-\s\d+\.?\d*)'
        targets = re.findall(targets_pattern, message_text)
        if len(targets) == 0:
            return new_message  # No targets found
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

    return new_message


def parse_reply_signal_message(message_text):
    """Parse replied message to signal message and returns parse result"""
    reply_match = re.search(Config.REPLY_MESSAGE_PATTERN, message_text)
    if reply_match:
        return reply_match.group(1)

    return None


def not_sent_channels(last_sent_ids):
    """Returns channels that don't have current message"""
    channels = []
    if last_sent_ids is None:
        return Config.DESTINATION_CHAT_ID, {}

    json_last_sent_ids = json.loads(last_sent_ids[0])
    for channel in Config.DESTINATION_CHAT_ID:
        if json_last_sent_ids.get(str(channel), None) is None:
            channels.append(channel)

    return channels, json_last_sent_ids
