from sqlalchemy import Column, Integer, BigInteger, String
from database import BASE, SESSION

NUMBER_OF_HASH_MESSAGE = 10


class MessageIdMap(BASE):
    """Model for message id(s) map from source channel to destination channel."""
    __tablename__ = "message_id_map"
    source__id = Column(BigInteger, primary_key=True)
    destination_id = Column(BigInteger, unique=True)


MessageIdMap.__table__.create(checkfirst=True)


class EditedMessageIdMap(BASE):
    """Model for edited message id(s) map from source channel to destination channel."""
    __tablename__ = "edited_message_id_map"
    source__id = Column(BigInteger, primary_key=True)
    destination_id = Column(BigInteger, unique=True)


EditedMessageIdMap.__table__.create(checkfirst=True)


class MessageHash(BASE):
    """Model for message hash to keep last (e.g 10) number of message hash
    to prevent from duplicated message entry caused by source channel."""
    __tablename__ = "message_hash"
    _id = Column(Integer, primary_key=True)
    msg_hash = Column(String(40), unique=True)


MessageHash.__table__.create(checkfirst=True)


async def get_message_map(msg_source_id):
    try:
        return SESSION.query(MessageIdMap.destination_id).filter_by(
            source__id=msg_source_id).first()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def add_message_map(msg_source_id, msg_destination_id):
    try:
        message_map = MessageIdMap()
        message_map.source__id = msg_source_id
        message_map.destination_id = msg_destination_id
        SESSION.add(message_map)
        SESSION.commit()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def add_edited_message_map(msg_source_id, msg_destination_id):
    try:
        message_map = EditedMessageIdMap()
        message_map.source__id = msg_source_id
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
            source__id=msg_source_id).first()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def message_hash_exist(_hash):
    try:
        return SESSION.query(MessageHash.msg_hash).filter_by(
            msg_hash=_hash).first()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()


async def add_message_hash(_hash):
    try:
        rows = SESSION.query(MessageHash).count()
        if rows >= NUMBER_OF_HASH_MESSAGE:
            max_id = SESSION.query(MessageHash).order_by(
                MessageHash._id.asc()).first()
            SESSION.query(MessageHash).filter_by(_id=max_id._id).delete()
            SESSION.commit()
        message_hash = MessageHash()
        message_hash.msg_hash = _hash
        SESSION.add(message_hash)
        SESSION.commit()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()
