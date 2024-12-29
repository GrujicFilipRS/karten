from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from data.db_session import SqlAlchemyBase
from datetime import datetime
from data import db_session
from data.users import User
from data.cards import Card


class Deck(SqlAlchemyBase):
    __tablename__ = 'deck'

    id = Column(Integer, primary_key=True)
    user_created_id = Column(Integer, ForeignKey("user.id"))
    name = Column(String, nullable=False)
    time_changed = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    description = Column(String, nullable=True)

    def to_dict(self):
        db_sess = db_session.create_session()
        user_created = db_sess.query(User).filter(User.id == self.user_created_id).first()
        cards = db_sess.query(Card).filter(Card.deck_id == self.id).all()
        cards_json = [card.to_dict() for card in cards]
        db_sess.close()

        deck_dict = {
            "deck_id": self.id,
            "deck_name": self.name,
            "user_created_name": user_created.username,
            "time_changed": self.time_changed.strftime("%Y-%m-%d %H:%M:%S"),
            "description": self.description,
            "cards": cards_json
        }
        return deck_dict
