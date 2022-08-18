import datetime
from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from database import BASE, SESSION


class MessageIdMap(BASE):
    """Model for message id(s) map from source channel to destination channel.
        Message hash is used to keep last (e.g 10) number of message hash
        to prevent from duplicated message entry caused by source channel."""
    __tablename__ = "message_id_map"
    source_id = Column(BigInteger, primary_key=True)
    destination_ids = Column(String(64))
    created_time = Column(DateTime, server_default=func.now())


MessageIdMap.__table__.create(checkfirst=True)


class ReplyMessageIdMap(BASE):
    """Model for replied message id(s) map from source channel to destination channel."""
    __tablename__ = "reply_message_id_map"
    source_id = Column(BigInteger, primary_key=True)
    destination_ids = Column(String(64))


ReplyMessageIdMap.__table__.create(checkfirst=True)


async def add_message_map(msg_source_id, msg_destination_ids):
    try:
        message_map = MessageIdMap()
        message_map.source_id = msg_source_id
        message_map.destination_ids = msg_destination_ids
        SESSION.add(message_map)
        SESSION.commit()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def update_message_map(msg_source_id, msg_destination_ids):
    try:
        update_query = SESSION.query(MessageIdMap).filter(
            MessageIdMap.source_id == msg_source_id).first()
        if update_query is None:
            return None
        update_query.destination_ids = msg_destination_ids
        SESSION.commit()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def get_message_map(msg_source_id):
    try:
        return SESSION.query(MessageIdMap.destination_ids).filter_by(
            source_id=msg_source_id).first()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def add_reply_message_map(msg_source_id, msg_destination_ids):
    try:
        message_map = ReplyMessageIdMap()
        message_map.source_id = msg_source_id
        message_map.destination_ids = msg_destination_ids
        SESSION.add(message_map)
        SESSION.commit()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def get_reply_message_map(msg_source_id):
    try:
        return SESSION.query(ReplyMessageIdMap.destination_ids).filter_by(
            source_id=msg_source_id).first()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def delete_old_rows():
    try:
        # Deletes old rows more than number of days
        expiration_days = 30
        limit = datetime.datetime.utcnow() - datetime.timedelta(days=expiration_days)

        print("deleted:  " + str(limit))
        return

        # Message map table
        SESSION.query(MessageIdMap).filter(
            MessageIdMap.created_time <= limit).delete()
        SESSION.commit()

        # Reply Message map table
        SESSION.query(ReplyMessageIdMap).filter(
            ReplyMessageIdMap.created_time <= limit).delete()
        SESSION.commit()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()
