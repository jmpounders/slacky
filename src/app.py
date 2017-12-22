import json
import requests

from flask import Flask, request, render_template, session

from common.database import Database
from models.user import User

app = Flask(__name__)
app.secret_key = "justin"

@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/login')
def login_template():
    return render_template('login.html')

@app.route('/register')
def register_template():
    return render_template('register.html')


@app.before_first_request
def initialize_database():
    Database.initialize()

@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
    else:
        session['email'] = None

    return render_template('profile.html', email=session['email'])

@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    User.register(email, password)

    return render_template('profile.html', email=session['email'])

@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        webhook = 'https://hooks.slack.com/services/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'
        msg = request.form['message']
        data = {'attachments': [{'fallback':'default text',
                                'title':'Title',
                                'pretext':'Pretext',
                                'text':'Text: '+msg}]}
        r = requests.post(webhook, data=json.dumps(data))

    return render_template('message.html')


if __name__ == '__main__':
    HOST = '127.0.0.1'
    PORT = 4000
    app.run(HOST, PORT)


