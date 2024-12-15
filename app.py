from flask import Flask, redirect, render_template
from data import db_session
from data.__all_models import User, Deck, Card

app = Flask(__name__)


@app.route('/')
def index():
    # TODO Ako korisnik nije ulogovan
    if True:
        return render_template('index.html')
    else:
        return redirect('/login')


@app.route('/login')
def login_page():
    # TODO Login
    if True:
        return render_template('login.html')
    else:
        return redirect('/dashboard')

@app.route('/signup')
def signup_page():
    # TODP Signup
    if True:
        return render_template('signup.html')
    else:
        return redirect('/dashboard')

if __name__ == '__main__':
    db_session.global_init("db/library.sqlite")
    app.run(debug=True, threaded=True)
