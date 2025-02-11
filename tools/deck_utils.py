from typing import List, Dict
from sqlalchemy.orm import Session
from data.__all_models import Deck, SavedDeck


def get_user_decks(user_id: int, db_sess: Session) -> List[Deck]:
    """
    Function for getting decks created by some user.

    :param user_id: ID of a user.
    :param db_sess: An active database session.
    :return: A list of Deck objects.
    """
    user_decks = db_sess.query(Deck).filter(Deck.user_created_id == user_id).all()
    return user_decks


def get_user_saved_decks(user_id: int, db_sess: Session) -> List[Deck]:
    """
    Function for getting decks saved by some user.

    :param user_id: ID of a user.
    :param db_sess: An active database session.
    :return: A list of Deck objects.
    """
    saved_decks = db_sess.query(SavedDeck).filter(SavedDeck.user_id == user_id).all()
    deck_ids = [saved_deck.deck_id for saved_deck in saved_decks]
    user_saved_decks = db_sess.query(Deck).filter(Deck.id.in_(deck_ids)).all()
    return user_saved_decks


def decks_to_dict(decks: List[Deck]) -> List[Dict]:
    """
    Transforms list of Deck objects to list of dicts.
    """
    return [deck.to_dict() for deck in decks]
