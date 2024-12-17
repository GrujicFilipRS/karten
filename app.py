from flask import Flask, redirect, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.__all_models import User, Deck, Card
from forms.user import UserLogInForm, UserSignUpForm
from config import config

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
    return render_template('dashboard.html', user=current_user.username)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    login_form = UserLogInForm()
    if login_form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            return redirect("/")
        return render_template(
            "login.html",
            login_form=login_form,
            message="false_mail_or_password"  # Ne postoji nalog sa takvim korisničkim imenom i šifrom
        )
    return render_template("login.html", login_form=login_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/signup')
def signup_page():
    # TODP Signup
    if True:
        return render_template('signup.html')
    else:
        return redirect('/')


if __name__ == '__main__':
    db_session.global_init("db/karten.sqlite")
    app.run(debug=True, threaded=True)
