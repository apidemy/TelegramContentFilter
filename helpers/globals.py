import asyncio
import threading
from database.messages_sql import delete_old_rows


def initialize():

    global lock_section
    lock_section = asyncio.Lock()

    # backup_message_id_thread()


""" Save current message id(s) in a thread by interval """


def backup_message_id_thread():
    delete_old_rows()
    interval = 3600  # 1 hour
    threading.Timer(10, backup_message_id_thread).start()
