from sqlalchemy import Column, Integer, BigInteger
from database import BASE, SESSION


class MessageIdMap(BASE):
    """Model for message id(s) map from source channel to destination channel."""
    __tablename__ = "message_id_map"
    # __table_args__ = {'extend_existing': True}
    source__id = Column(BigInteger, primary_key=True)
    destination_id = Column(BigInteger, unique=True)
    id = Column(Integer, unique=True)

    # def __init__(self, user_id, channels=None):
    #     self.user_id = user_id
    #     self.channels = channels

    # def __repr__(self):
    # return "<MessageIdMap(source__id='%s', destination_id='%s')>" % (self.source__id, self.destination_id)


MessageIdMap.__table__.create(checkfirst=True)


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
        message_map = {MessageIdMap.source__id: msg_source_id,
                       MessageIdMap.destination_id: msg_destination_id}
        SESSION.add(message_map)
        SESSION.commit()
    except:
        SESSION.rollback()
        raise
    finally:
        SESSION.close()
