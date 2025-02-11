from typing import FrozenSet, List, Dict
from nltk import download, word_tokenize
from nltk.stem.snowball import EnglishStemmer
from sqlalchemy.orm import Session
from data.__all_models import Deck

download('punkt_tab', quiet=True)


def tokenize(text: str) -> FrozenSet[str]:
    """
    Tokenizes a given text by splitting it into words, stemming them,
    and returning a frozen set of alphanumeric tokens.

    :param text: The input text to tokenize.
    :return: A frozen set of stemmed and alphanumeric tokens.
    """
    return frozenset(EnglishStemmer().stem(i) for i in word_tokenize(text) if i.isalnum())


def tokenize_all_decks(db_sess: Session) -> Dict[int, FrozenSet[str]]:
    """
    Tokenizes the names of all decks from the database
    :param db_sess: An active database session.
    :return: A dictionary with deck IDs as keys and tokenized deck names as values.
    """
    all_decks = db_sess.query(Deck).all()
    return {deck.id: tokenize(deck.name) for deck in all_decks}


def search_decks(search_text: str, tokens_index: Dict[int, FrozenSet[str]], db_sess: Session) -> List[Deck]:
    """
    Searches for decks matching the given search text based on token similarity.

    :param search_text: The text to search for.
    :param tokens_index: A dictionary mapping deck IDs to sets of tokenized words.
    :param db_sess: An active database session.
    :return: A list of matching Deck objects sorted by relevance.
    """
    matching_decks_dicts = []
    search_tokens = tokenize(search_text)

    for deck_id, tokens in tokens_index.items():
        num_matching_words = len(search_tokens & tokens)
        if num_matching_words > 0:
            matching_decks_dicts.append({"deck_id": deck_id, "num_matching_words": num_matching_words})

    # Sort results by the number of matching words in descending order
    matching_decks_dicts.sort(key=lambda x: x["num_matching_words"], reverse=True)
    deck_ids = [i["deck_id"] for i in matching_decks_dicts]

    if not deck_ids:
        return []

    # Fetch matching decks from the database
    search_results = db_sess.query(Deck).filter(Deck.id.in_(deck_ids)).all()
    return search_results
