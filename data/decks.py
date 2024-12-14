from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from data.db_session import SqlAlchemyBase
from datetime import datetime


class Deck(SqlAlchemyBase):
    __tablename__ = 'deck'

    id = Column(Integer, primary_key=True)
    user_created_id = ForeignKey("user.id")
    name = Column(String, nullable=False)
    time_changed = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
