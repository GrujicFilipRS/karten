from sqlalchemy import Column, Integer, String, ForeignKey
from data.db_session import SqlAlchemyBase


class Card(SqlAlchemyBase):
    __tablename__ = "card"

    id = Column(Integer, primary_key=True)
    deck_id = Column(Integer, ForeignKey("deck.id"))
    position = Column(Integer, nullable=False)
    front = Column(String, nullable=False)
    back = Column(String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'deck_id': self.deck_id,
            'position': self.position,
            'front': self.front,
            'back': self.back
        }
