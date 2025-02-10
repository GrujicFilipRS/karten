from flask import Flask, redirect, render_template, request, flash, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from json import dumps as json_dumps

from data import db_session
from data.__all_models import User, Deck, Card, SavedDeck
from forms.user import UserLogInForm, UserSignUpForm
from config import config
from tools import search, deck_utils, user_service
from api.routes import api_bp

template_dir = "templates"
static_dir = "static"

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.tokens_index = {}
app.register_blueprint(api_bp, url_prefix='/api')

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    db_sess.close()
    return user


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
@login_required
def dashboard():
    db_sess = db_session.create_session()

    user_decks = deck_utils.get_user_decks(current_user.id, db_sess)
    user_saved_decks = deck_utils.get_user_saved_decks(current_user.id, db_sess)

    user_decks_dicts = deck_utils.decks_to_dict(user_decks)
    user_saved_decks_dicts = deck_utils.decks_to_dict(user_saved_decks)

    db_sess.close()

    return render_template(
        "dashboard.html",
        title="Dashboard",
        user=current_user.id,
        user_decks=user_decks_dicts,
        other_decks=user_saved_decks_dicts
    )


@app.route('/deck/<int:deck_id>')
@login_required
def view_deck(deck_id: int):
    db_sess = db_session.create_session()
    deck = db_sess.query(Deck).filter(Deck.id == deck_id).first()
    db_sess.close()

    if not deck:
        return "-1"

    deck_dict = deck.to_dict()
    is_my_deck = deck.user_created_id == current_user.id

    if request.args.get("secret") == config.BOT_SECRET:
        return json_dumps(deck_dict)

    return render_template(
        "view_deck.html",
        deck=deck_dict,
        is_my_deck=is_my_deck,
        title=f"Flashcards {deck_dict['deck_name']}"
    )


@app.route('/deck/<int:deck_id>/edit')
@login_required
def edit_deck(deck_id: int):
    db_sess = db_session.create_session()
    deck = db_sess.query(Deck).filter(Deck.id == deck_id).first()
    user = db_sess.query(User).filter(User.id == deck.user_created_id).first()
    db_sess.close()
    if user.id != current_user.id:
        flash('You do not have permission to edit this deck.')
        return redirect(url_for('view_deck', deck_id=deck_id))

    # if request.method == 'POST':
    #     # TODO logic for getting the information about decks from js
    #     pass
    #
    #     db.session.commit()
    #     flash('Deck updated successfully.')
    #     return redirect(f'/deck/{deck_id}')

    return render_template('deck_edit.html', deck=deck)


@app.route('/deck/<int:deck_id>/delete')
@login_required
def delete_deck(deck_id: int):
    db_sess = db_session.create_session()
    deck = db_sess.query(Deck).filter(Deck.id == deck_id).first()
    user = db_sess.query(User).filter(User.id == deck.user_created_id).first()
    db_sess.close()
    if user.id != current_user.id:
        flash('You do not have permission to edit this deck.')
        return redirect(url_for('view_deck', deck_id=deck_id))
    db_sess.delete(deck)
    return redirect(url_for('dashboard'))


@app.route('/login', methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    login_form = UserLogInForm()
    if login_form.validate_on_submit():
        username_data = login_form.username.data
        password_data = login_form.password.data
        remember_me_data = login_form.remember_me.data

        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == username_data).first()
        db_sess.close()
        if not (user and user.check_password(password_data)):
            return render_template(
                'login_signup.html',
                form_action=url_for('login_page'),
                form_class='login-form',
                title='Login',
                form=login_form,
                message="false_mail_or_password"
            )
        login_user(user, remember=remember_me_data)
        return redirect(url_for('index'))
    return render_template(
        'login_signup.html',
        form_action=url_for('login_page'),
        form_class='login-form',
        title='Login',
        form=login_form
    )


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    sign_up_form = UserSignUpForm()
    if sign_up_form.validate_on_submit():
        username_data = sign_up_form.username.data
        password_data = sign_up_form.password.data

        db_sess = db_session.create_session()
        existing_user = db_sess.query(User).filter(User.username == username_data).first()
        if existing_user is not None:
            return render_template(
                'login_signup.html',
                form_class="signup-form",
                title="Sign up",
                message="username_exists",
                form=sign_up_form,
            )
        user_service.register_user(username_data, password_data, db_sess)
        db_sess.close()

        return redirect(url_for('dashboard'))
    return render_template(
        'login_signup.html',
        form_class="signup-form",
        title="Sign up",
        form=sign_up_form,
    )


@app.route('/search/<string:search_text>', methods=["GET", "POST"])
def search_decks(search_text: str):
    db_sess = db_session.create_session()
    search_results = search.search_decks(search_text, app.tokens_index, db_sess)
    db_sess.close()

    return render_template(
        "search.html",
        search_results=search_results,
        search_text=search_text,
        title=f"Search results: {search_text}"
    )


@app.route('/search', methods=['GET'])
def search_ui():
    return render_template(
        'search_ui.html',
    )


if __name__ == '__main__':
    db_session.global_init("db/karten.sqlite")

    sess = db_session.create_session()
    decks = sess.query(Deck).all()
    app.tokens_index = {deck.id: search.tokenize(deck.name) for deck in decks}
    sess.close()

    app.run(debug=True, threaded=True)
