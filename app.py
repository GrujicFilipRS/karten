from flask import Flask, redirect, render_template
import flask

app = Flask(__name__)

@app.route('/')
def index():
    # Ako korisnik nije ulogovan, TODO
    if True:
        return render_template('index.html')
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run()