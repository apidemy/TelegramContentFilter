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
    destination_id = Column(BigInteger, unique=True)
    msg_hash = Column(String(40), unique=True)
    created_time = Column(DateTime, server_default=func.now())


MessageIdMap.__table__.create(checkfirst=True)


class EditedMessageIdMap(BASE):
    """Model for edited message id(s) map from source channel to destination channel."""
    __tablename__ = "edited_message_id_map"
    source_id = Column(BigInteger, primary_key=True)
    destination_id = Column(BigInteger, unique=True)


EditedMessageIdMap.__table__.create(checkfirst=True)


async def get_message_map(msg_source_id):
    try:
        return SESSION.query(MessageIdMap.destination_id).filter_by(
            source_id=msg_source_id).first()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def add_message_map(msg_source_id, msg_destination_id, _hash):
    try:
        exist = SESSION.query(MessageIdMap.msg_hash).filter_by(
            msg_hash=_hash).first()

        if exist:
            return exist

        message_map = MessageIdMap()
        message_map.source_id = msg_source_id
        message_map.destination_id = msg_destination_id
        message_map.msg_hash = _hash
        SESSION.add(message_map)
        SESSION.commit()

        # Deletes old rows more than number of days
        expiration_days = 30
        limit = datetime.datetime.utcnow() - datetime.timedelta(days=expiration_days)
        SESSION.query(MessageIdMap).filter(
            MessageIdMap.created_time <= limit).delete()
        SESSION.commit()

    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def is_message_exist(_hash):
    try:
        return SESSION.query(MessageIdMap.msg_hash).filter_by(
            msg_hash=_hash).first()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def add_edited_message_map(msg_source_id, msg_destination_id):
    try:
        message_map = EditedMessageIdMap()
        message_map.source_id = msg_source_id
        message_map.destination_id = msg_destination_id
        SESSION.add(message_map)
        SESSION.commit()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def get_edited_message_map(msg_source_id):
    try:
        return SESSION.query(EditedMessageIdMap.destination_id).filter_by(
            source_id=msg_source_id).first()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()
