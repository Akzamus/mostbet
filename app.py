from settings import BOT_TOKEN, USER_ID, WEB_HOOK_URL, APP_HOST, APP_PORT
from flask import Flask, request, make_response

import atexit
import os
import telebot
import flask
import time


chat_id = 0
chat_id_file = 'chat_id.txt'

bot = telebot.TeleBot(token=BOT_TOKEN)
app = Flask(__name__)


def save_chat_id():
    with open(chat_id_file, 'w') as file:
        file.write(str(chat_id))


if os.path.isfile(chat_id_file):
    with open(chat_id_file, 'r') as f:
        chat_id = int(f.read().strip())
else:
    chat_id = 0
atexit.register(save_chat_id)


@app.route('/notify/telegram/', methods=['GET'])
def handle_get_request():
    if chat_id == 0:
        return make_response('Error: chat_id not set', 400)

    params = request.args
    message = f'Получен GET запрос с параметрами: {params}'
    bot.send_message(chat_id, message)

    return make_response('OK', 200)


@app.route('/', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') != 'application/json':
        return make_response('Error: content-type is not json', 403)

    json_string = flask.request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])

    return make_response('OK', 200)


@bot.message_handler(commands=['start'])
def register_chat(message):
    message_text = 'You are not an administrator'

    if message.from_user.id == int(USER_ID):
        global chat_id
        chat_id = message.chat.id
        message_text = 'The chat is registered'

    bot.send_message(message.chat.id, message_text)


if __name__ == '__main__':
    bot.remove_webhook()
    time.sleep(0.1)

    bot.set_webhook(url=WEB_HOOK_URL)
    app.run(host=APP_HOST, port=APP_PORT)
