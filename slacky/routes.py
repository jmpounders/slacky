from flask import request, render_template, make_response, session, flash

from .common.database import Database
from .common.slack import Slack
from .models.user import User
from .models.lesson import Lesson
from .models.cfu import CFUMessage, FreeResponseCFU, MultipleChoiceCFU

from . import app

# TODO Add oauth for slack (for more than one user)
#      Store user tokens in mongo

@app.before_first_request
def initialize_database():
    """Initialize the database connection and Slack client."""
    Database.initialize()
    Slack.initialize(app.config['SLACK_TOKEN'])

@app.route('/install', methods=['GET'])
def pre_install():
    client_id = app.config['SLACK_CLIENT_ID']
    scope = app.config['SLACK_SCOPE']
    return render_template("install.html", client_id=client_id, scope=scope, username=username)

#@app.route('/post-install', methods=['POST'])
#def post_install():
#    code = request.args.get('code')
#    user.slack_auth(code)
#    return

@app.route('/')
def home_template():
    """Landing page."""
    return render_template('home.html')

@app.route('/login')
def login_template():
    """Present the login prompt."""
    return render_template('login.html')

@app.route('/register')
def register_template():
    """Present the registration prompt."""
    return render_template('register.html')


@app.route('/auth/login', methods=['POST'])
def login_user():
    """Receives login credentials and redirects to the lessons
    page if successful."""
    username = request.form['username']
    password = request.form['password']

    if User.login_valid(username, password):
        user = User.login(username)
    else:
        session['username'] = None
        return render_template('home.html')

    return make_response(user_lessons(user._id))

@app.route('/auth/register', methods=['POST'])
def register_user():
    """Receives registration request and redirects to the
    lessons page if successful."""
    username = request.form['username']
    password = request.form['password']

    if User.register(username, password):
        user = User.login(username)
    else:
        session['username'] = None
        return render_template('home.html')

    return make_response(user_lessons(user._id))

@app.route('/lessons/<string:user_id>')
@app.route('/lessons')
def user_lessons(user_id=None, channel=None):
    """Page showing user's lessons."""
    session['lesson_id'] = None

    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_username(session['username'])

    lessons = user.get_lessons()

    return render_template("user_lessons.html",
                           lessons=lessons, username=user.username, channel=channel)

@app.route('/lessons/new', methods=['POST', 'GET'])
def create_new_lesson():
    if request.method == 'GET':
        return render_template('new_lesson.html')
    else:
        title = request.form['title']
        user = User.get_by_username(session['username'])

        new_lesson = Lesson(user.username, title, user._id)
        new_lesson.save_to_mongo()

        return make_response(user_lessons(user._id))

@app.route('/lessons/delete/<string:lesson_id>')
def delete_lesson(lesson_id):
    Lesson.delete_from_mongo(lesson_id)
    return make_response(user_lessons())

@app.route('/lessons/rename/<string:lesson_id>', methods=['POST'])
def rename_lesson(lesson_id):
    new_name = request.form['new_name']
    lesson = Lesson.from_mongo(lesson_id)
    lesson.update({'title': new_name})

    return make_response(lesson_cfus(lesson_id))


@app.route('/cfus/<string:lesson_id>')
def lesson_cfus(lesson_id, lesson_title=None):
    if lesson_title is not None:
        pass

    session['lesson_id'] = lesson_id
    lesson = Lesson.from_mongo(lesson_id)
    cfus = lesson.get_cfus()

    return render_template('cfus.html', cfus=cfus,
                           lesson_title=lesson.title, lesson_id=lesson._id)

@app.route('/cfus/new_fr/<string:lesson_id>', methods=['POST', 'GET'])
def creat_new_cfu(lesson_id):
    if request.method == 'GET':
        return render_template('new_cfu_fr.html', lesson_id=lesson_id)
    else:
        title = request.form['title']
        message = request.form['message']
        user = User.get_by_username(session['username'])

        new_cfu = FreeResponseCFU(message, user._id, lesson_id)
        new_cfu.save_to_mongo()

        return make_response(lesson_cfus(lesson_id))

@app.route('/cfus/new_mc/<string:lesson_id>', methods=['POST', 'GET'])
def creat_new_cfu_mc(lesson_id):
    if request.method == 'GET':
        return render_template('new_cfu_mc.html', lesson_id=lesson_id)
    else:
        title = request.form['title']
        question = request.form['question']
        options = []
        for i in range(4):
            options.append(request.form['option'+str(i+1)])

        user = User.get_by_username(session['username'])

        new_cfu = MultipleChoiceCFU(question, options, user._id, lesson_id)
        new_cfu.save_to_mongo()

        return make_response(lesson_cfus(lesson_id))

@app.route('/cfus/delete/<string:cfu_id>')
def delete_cfu(cfu_id):
    CFUMessage.delete_from_mongo(cfu_id)
    return make_response(lesson_cfus(session['lesson_id']))

@app.route('/cfus/post/<string:cfu_id>')
def post_cfu(cfu_id):
    cfu = CFUMessage.get_from_mongo(cfu_id)
    cfu.post()
    return make_response(lesson_cfus(session['lesson_id']))


# ===== DEPRECATED ======
#@app.route('/message', methods=['GET', 'POST'])
#def message():
#    if request.method == 'POST':
#        webhook = 'https://hooks.slack.com/services/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'
#        msg = request.form['message']
#        data = {'attachments': [{'fallback':'default text',
#                                 'title':'Title',
#                                 'pretext':'Pretext',
#                                 'text':'Text: '+msg}]}
#        r = requests.post(webhook, data=json.dumps(data))
#
#    return render_template('message.html')
# ========================



