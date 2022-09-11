
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
@app.route('/index/')
def hello():
    return '<h1>Hello, World!</h1>'

@app.route('/about/')
def about():
    return '<h3>This is a Flask web application.</h3>'


@app.route('/test/')
def testing_template():
    return render_template('index.html')





#REAL SHIT
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/home')
def home_page():
    return render_template('homepage.html')