from flask import Flask, redirect, render_template
import flask

app = Flask(__name__)

@app.route('/')
def index():
    # TODO Ako korisnik nije ulogovan
    if True:
        return render_template('index.html')
    else:
        return redirect('/login')

@app.route('/login')
def login():
    # TODO Login
    if True:
        return render_template('login.html')
    else:
        return redirect('/dashboard')

if __name__ == '__main__':
    app.run()