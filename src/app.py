import json
import requests

from flask import Flask, request, render_template, make_response, session

from common.database import Database
from models.user import User
from models.lesson import Lesson
from models.cfu import CFUMessage

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

@app.route('/lessons/<string:user_id>')
@app.route('/lessons')
def user_lessons(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])

    lessons = user.get_lessons()

    return render_template("user_lessons.html",
                           lessons=lessons, email=user.email)

@app.route('/lessons/new', methods=['POST', 'GET'])
def create_new_lesson():
    if request.method == 'GET':
        return render_template('new_lesson.html')
    else:
        title = request.form['title']
        user = User.get_by_email(session['email'])

        new_lesson = Lesson(user.email, title, user._id)
        new_lesson.save_to_mongo()

        return make_response(user_lessons(user._id))

@app.route('/cfus/<string:lesson_id>')
def lesson_cfus(lesson_id):
    lesson = Lesson.from_mongo(lesson_id)
    cfus = lesson.get_cfus()

    return render_template('cfus.html', cfus=cfus,
                           lesson_title=lesson.title, lesson_id=lesson._id)

@app.route('/cfus/new/<string:lesson_id>', methods=['POST', 'GET'])
def creat_new_cfu(lesson_id):
    if request.method == 'GET':
        return render_template('new_cfu.html', lesson_id=lesson_id)
    else:
        title = request.form['title']
        message = request.form['message']
        user = User.get_by_email(session['email'])

        new_cfu = CFUMessage(title, message, user._id, lesson_id)
        new_cfu.save_to_mongo()

        return make_response(lesson_cfus(lesson_id))

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


