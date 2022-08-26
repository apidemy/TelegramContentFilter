import asyncio
import threading
from database.messages_sql import delete_old_rows


def initialize():

    global lock_section
    lock_section = asyncio.Lock()

    backup_message_id_thread()


def backup_message_id_thread():
    """ Delete old message id(s) to reduce storage usage in a thread by interval """
    delete_old_rows()
    interval = 3600 * 24 * 7  # 1 Week
    _thread = threading.Timer(interval, backup_message_id_thread)
    _thread.setDaemon(True)
    _thread.start()
