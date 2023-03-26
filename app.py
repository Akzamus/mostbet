from settings.settings import admin_ids, WEB_HOOK_URL, APP_HOST, APP_PORT
from flask import Flask, request, make_response
from telegram_bot import bot, send_notification_to_admins

import telebot
import flask
import time

app = Flask(__name__)


def check_user_existence(user_id):
    user_exists = True
    try:
        bot.send_message(user_id, 'Now you are an admin')
    except telebot.apihelper.ApiException:
        user_exists = False
    return user_exists


@app.route('/notify/telegram/after_registration', methods=['GET'])
def send_notification_after_registration_use_telegram_bot():
    user_id = request.args.get('user_id', '', str)
    if user_id == '':
        return make_response('Bad Request', 400)
    response_text = f'The user has registered, id: {user_id}'

    try:
        send_notification_to_admins(response_text)
    except telebot.apihelper.ApiException:
        return make_response('Error: failed to send notification to admin', 400)

    return make_response('OK', 200)


@app.route('/notify/telegram/after_first_deposit', methods=['GET'])
def send_notification_after_first_deposit_use_telegram_bot():
    user_id = request.args.get('user_id', '', str)
    amount = request.args.get('amount', 0, int)
    currency = request.args.get('currency', '', str)

    if user_id == '' or amount == 0 or currency == '':
        return make_response('Bad Request', 400)

    response_text = f'User id: {user_id}\n' \
                    f'Amount: {amount} {currency}'

    try:
        send_notification_to_admins(response_text)
    except telebot.apihelper.ApiException:
        return make_response('Error: failed to send notification to admin', 400)

    return make_response('OK', 200)


@app.route('/', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') != 'application/json':
        return make_response('Error: content-type is not json', 403)

    try:
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
    except Exception:
        return make_response('Error: failed to process update', 400)

    return make_response('OK', 200)


if __name__ == '__main__':
    bot.remove_webhook()
    time.sleep(0.1)

    bot.set_webhook(url=WEB_HOOK_URL)
    app.run(host=APP_HOST, port=APP_PORT)
