import asyncio
import threading


def initialize():

    global lock_section
    lock_section = asyncio.Lock()


""" Save current message id(s) in a thread by interval """


def backup_message_id_thread():
    print("hello")
    interval = 3600  # 1 hour
    threading.Timer(3, backup_message_id_thread).start()
