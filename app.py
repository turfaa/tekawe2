import os
import sys
from argparse import ArgumentParser

from flask import Flask
from flask import url_for
from flask import session
from flask import make_response
from flask import request
from flask import redirect
from flask import flash

from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from myconfig import channel_secret, channel_access_token
from myconfig import ACTION_CREATE_GAME, ACTION_START_GAME, ACTION_JOIN_GAME, ACTION_GUESS
from dbhandler import dbhandler

app = Flask(__name__)
app.secret_key = os.urandom(22)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)
db = dbhandler()

@app.route('/')
def index():
    flash('ganteng')
    return make_response('Hello, World! {}'.format(url_for('index')))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)


    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        if (not(db.getPlayerName(event.source.user_id))):
            name = line_bot_api.get_profile(event.source.user_id).display_name
            db.addPlayer(event.source.user_id, name)

        db.addIn(event.source.user_id, event.message.text)

        splitted = event.message.text.split()
        if (splitted[0] == '/baru'):
            db.addAction(event.source.user_id, ACTION_CREATE_GAME)
        elif (splitted[0] == '/mulai'):
            db.addAction(event.source.user_id, ACTION_START_GAME)
        elif (splitted[0] == '/join'):
            if (len(splitted) > 1):
                db.addAction(event.source.user_id, ACTION_JOIN_GAME, splitted[1])
            else:
                db.addOut(event.source.user_id, 'Tulis "/join <token>" untuk bergabung dengan game yang sudah ada atau "/baru" untuk memulai game yang baru.')
        elif (splitted[0] == '/help'):
            db.addOut(event.source.user_id, 'Daftar perintah:\n/baru : membuat permainan baru\n/mulai : memulai permainan\n/join <token> : memasuki permainan yang sudah dibuat orang lain\n/help : bantuan')
        else:
            db.addAction(event.source.user_id, ACTION_GUESS, ' '.join(splitted))

    return 'OK'

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)
