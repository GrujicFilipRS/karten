from sqlalchemy import Column, Integer, DateTime, ForeignKey
from data.db_session import SqlAlchemyBase
from datetime import datetime


class SavedDeck(SqlAlchemyBase):
    __tablename__ = "savedDeck"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    deck_id = Column(Integer, ForeignKey("deck.id"))
    saved_at = Column(DateTime, default=datetime.utcnow)
