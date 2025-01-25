from flask import Blueprint, jsonify, request

from data import db_session
from data.__all_models import Deck, SavedDeck

api_bp = Blueprint('api', __name__)


@api_bp.route('/api/saved_decks', methods=['GET'])
def get_saved_deck():
    try:
        data = request.get_json()
        if not data or 'deck_id' not in data or 'user_id' not in data:
            return jsonify({
                "success": False,
                "message": "Invalid request: 'deck_id' and 'user_id' are required"
            }), 400

        db_sess = db_session.create_session()
        saved_deck = db_sess.query(SavedDeck).filter_by(
            user_id=data['user_id'],
            deck_id=data['deck_id']
        ).first()
        db_sess.close()

        if not saved_deck:
            return jsonify({
                "success": False,
                "message": "Deck not found."
            }), 404

        # Return the SavedDeck data as JSON
        return jsonify({
            "success": True,
            "id": saved_deck.id,
            "user_id": saved_deck.user_id,
            "deck_id": saved_deck.deck_id,
            "saved_at": saved_deck.saved_at.isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404


@api_bp.route('/api/saved_deck', methods=['POST'])
def create_saved_deck():
    try:
        data = request.get_json()  # Get JSON data from the request
        if not data or 'user_id' not in data or 'deck_id' not in data:
            return jsonify({
                "success": False,
                "message": "Invalid request: 'user_id' and 'deck_id' are required."
            }), 400

        user_id = data.get('user.id')
        deck_id = data.get('deck_id')

        db_sess = db_session.create_session()
        deck = db_sess.query(Deck).get(deck_id)

        if deck is None:
            db_sess.close()
            return jsonify({
                "success": False,
                "message": "Deck not found."
            }), 404

        # Check if the deck is already in the user's library
        saved_deck = db_sess.query(SavedDeck).filter_by(
            user_id=user_id,
            deck_id=deck_id
        ).first()

        if saved_deck:
            db_sess.close()
            return jsonify({
                "success": False,
                "message": "Deck not found."
            }), 404

        # If the deck is not in, add it
        new_library_entry = SavedDeck(user_id=id, deck_id=deck_id)
        db_sess.add(new_library_entry)
        db_sess.commit()
        db_sess.close()
        return jsonify({
            "success": True,
            "message": "Deck added to your library!",
            "action": 'added'
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404


@api_bp.route('/api/saved_deck', methods=['DELETE'])
def delete_created_deck():
    # TODO задокументировать структуру json запроса и ответа
    try:
        data = request.get_json()  # Get JSON data from the request
        if not data or 'user_id' not in data or 'deck_id' not in data:
            return jsonify({
                "success": False,
                "message": "Invalid request: 'user_id' and 'deck_id' are required."
            }), 400

        user_id = data.get('user.id')
        deck_id = data.get('deck_id')

        db_sess = db_session.create_session()
        deck = db_sess.query(Deck).get(deck_id)

        if deck is None:
            db_sess.close()
            return jsonify({
                "success": False,
                "message": "Deck not found."
            }), 404

        # Check if the deck is already in the user's library
        saved_deck = db_sess.query(SavedDeck).filter_by(
            user_id=user_id,
            deck_id=deck_id
        ).first()

        if not saved_deck:
            db_sess.close()
            return jsonify({
                "success": False,
                "message": "Deck is not in user's library."
            }), 404

        # If the deck is already in, remove it
        db_sess.delete(saved_deck)
        db_sess.commit()
        db_sess.close()
        return jsonify({
            "success": True,
            "message": "Deck removed from your library!",
            "action": 'removed'
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 404
