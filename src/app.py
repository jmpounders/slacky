import json
import requests
from flask import Flask, request, make_response, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

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


