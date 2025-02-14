from flask import Blueprint, jsonify, request
from flask_login import current_user

from data import db_session
from data.__all_models import Card, Deck, SavedDeck

api_bp = Blueprint('api', __name__)


@api_bp.route('/saved_deck', methods=['GET'])
def get_saved_deck():
    try:
        print("OK")
        user_id = request.args.get('user_id')
        deck_id = request.args.get('deck_id')
        print(f"GET OK: {user_id}, {deck_id}")

        if not user_id or not deck_id:
            return jsonify({
                "message": "Invalid request: 'user_id' and 'deck_id' are required"
            }), 400

        db_sess = db_session.create_session()
        saved_deck = db_sess.query(SavedDeck).filter_by(
            user_id=user_id,
            deck_id=deck_id
        ).first()
        db_sess.close()

        if not saved_deck:
            return jsonify({
                "message": "Deck not found."
            }), 404

        # Возвращаем данные о сохраненной колоде
        return jsonify({
            "id": saved_deck.id,
            "user_id": saved_deck.user_id,
            "deck_id": saved_deck.deck_id,
            "saved_at": saved_deck.saved_at.isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500


@api_bp.route('/saved_deck', methods=['POST'])
def create_saved_deck():
    try:
        user_id = request.args.get('user_id')
        deck_id = request.args.get('deck_id')

        if not user_id or not deck_id:
            return jsonify({
                "message": "Invalid request: 'user_id' and 'deck_id' are required."
            }), 400

        db_sess = db_session.create_session()
        deck = db_sess.query(Deck).get(deck_id)

        if deck is None:
            db_sess.close()
            return jsonify({
                "message": "Deck not found."
            }), 404

        # Check if SavedDeck already exists
        saved_deck = db_sess.query(SavedDeck).filter_by(
            user_id=user_id,
            deck_id=deck_id
        ).first()

        if saved_deck:
            db_sess.close()
            return jsonify({
                "message": "Deck already in user's library."
            }), 400

        # Is not, add it
        new_library_entry = SavedDeck(user_id=user_id, deck_id=deck_id)
        db_sess.add(new_library_entry)
        db_sess.commit()
        db_sess.close()
        return jsonify({
            "message": "Deck added to your library!",
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500


@api_bp.route('/saved_deck', methods=['DELETE'])
def delete_created_deck():
    try:
        saved_deck_id = request.args.get('saved_deck_id')

        if not id:
            return jsonify({
                "message": "Invalid request: 'saved_deck_id' is required."
            }), 400

        db_sess = db_session.create_session()

        # Check if SavedDeck already exists
        saved_deck = db_sess.query(SavedDeck).get(saved_deck_id)

        if not saved_deck:
            db_sess.close()
            return jsonify({
                "message": "Deck is not in user's library."
            }), 404

        # If exists, delete it
        db_sess.delete(saved_deck)
        db_sess.commit()
        db_sess.close()
        return jsonify({
            "message": "Deck removed from your library!",
        }), 200

    except Exception as e:
        return jsonify({
            "message": str(e)
        }), 500


@api_bp.route('/deck', methods=['POST'])
def create_deck_api():
    db_sess = db_session.create_session()
    try:
        data = request.json
        deck_name = data.get("deck_name")
        deck_description = data.get("description")
        cards = data.get("cards", [])

        new_deck = Deck(
            user_created_id=current_user.id,
            name=deck_name,
            description=deck_description
        )
        db_sess.add(new_deck)
        db_sess.flush()  # Get the ID before commit

        for position, card in enumerate(cards):
            new_card = Card(
                deck_id=new_deck.id,
                position=position,
                front=card["front"],
                back=card["back"]
            )
            db_sess.add(new_card)
        db_sess.commit()
        return jsonify({"success": True}), 200
    except Exception as e:
        db_sess.rollback()
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
    finally:
        db_sess.close()
