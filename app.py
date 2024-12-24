from flask import Flask, redirect, render_template, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.__all_models import User, Deck, Card
from forms.user import UserLogInForm, UserSignUpForm
from config import config
from json import dumps as json_dumps
from datetime import datetime

template_dir = "templates"
static_dir = "static"
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = config.SECRET_KEY

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('index.html')

    db_sess = db_session.create_session()
    user_decks = db_sess.query(Deck).filter(Deck.user_created_id == current_user.id).all()
    other_decks = db_sess.query(Deck).filter(Deck.user_created_id != current_user.id).all()
    user_decks_dicts = [deck.to_dict() for deck in user_decks]
    other_decks_dicts = [deck.to_dict() for deck in other_decks]

    return render_template(
        'dashboard.html',
        user=current_user.id,
        user_decks=user_decks_dicts,
        other_decks=other_decks_dicts
    )


# TODO: deck to json function

@app.route('/deck/<int:deck_id>')
def view_deck(deck_id: int):
    db_sess = db_session.create_session()
    deck = db_sess.query(Deck).filter(Deck.id == deck_id).first()

    if not deck:
        return "-1"

    deck_dict = deck.to_dict()

    if request.args.get("secret") == config.BOT_SECRET:
        return json_dumps(deck_dict)

    return render_template("view_deck.html", deck=deck_dict)


@app.route('/deck/<int:deck_id>/edit')
@login_required
def edit_deck(deck_id: int):
    db_sess = db_session.create_session()
    deck = db_sess.query(Deck).filter(Deck.id == deck_id).first()
    user = db_sess.query(User).filter(User.id == deck.user_created_id).first()
    if user.id != current_user.id:
        flash('You do not have permission to edit this deck.')
        return redirect(f'/deck/{deck_id}')

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
    if user.id != current_user.id:
        flash('You do not have permission to edit this deck.')
        return redirect(f'/deck/{deck_id}')
    db_sess.delete(deck)
    return redirect('/dashboard')


@app.route('/login', methods=["GET", "POST"])
def login_page():
    if current_user.is_authenticated:
        return redirect('/dashboard')

    login_form = UserLogInForm()
    if login_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.username == login_form.username.data).first()
        if not (user and user.check_password(login_form.password.data)):
            return render_template(
                "login.html",
                login_form=login_form,
                message="false_mail_or_password"
            )
        login_user(user, remember=login_form.remember_me.data)
        return redirect("/")
    return render_template("login.html", login_form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/signup', methods=["GET", "POST"])
def signup_page():
    if current_user.is_authenticated:
        return redirect('/dashboard')

    sign_up_form = UserSignUpForm()
    if sign_up_form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == sign_up_form.username.data).first() is not None:
            return render_template(
                'signup.html',
                message="username_exists",
                sign_up_form=sign_up_form
            )
        user = User(username=sign_up_form.username.data)
        user.set_password(sign_up_form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('signup.html', sign_up_form=sign_up_form)


if __name__ == '__main__':
    db_session.global_init("db/karten.sqlite")
    app.run(debug=True, threaded=True)
