import time
import threading


def initialize():
    global messages_map_id
    global current_hashes
    global edited_message_map

    messages_map_id = {}
    edited_message_map = {}
    current_hashes = []


def store_to_db():
    print("hello")
    # await add_message_map(msg.message_id, sent.message_id)
    # await get_message_map(msg.reply_to_message.message_id)
    # msg_id = await get_edited_message_map(msg.message_id)
    # await add_edited_message_map(msg.message_id, sent.message_id)

    # threading.Timer(3, store_to_db).start()
