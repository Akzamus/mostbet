from flask import Flask, request, make_response, Response
from telebot.apihelper import ApiException
from telegram_bot import TelegramBot
from telebot.types import Update
import flask


class TelegramWebhookHandler:
    def __init__(self, telegram_bot: TelegramBot) -> None:
        self.__app: Flask = Flask(__name__)
        self.__bot: TelegramBot = telegram_bot

        @self.__app.route('/notify/telegram/after_registration', methods=['GET'])
        def send_notification_after_registration_use_telegram_bot() -> Response:
            user_id: str = request.args.get('user_id', '', str)

            if user_id == '':
                return make_response('Bad Request', 400)
            response_text: str = f'The user has registered, id: {user_id}'

            try:
                self.__bot.send_notification_to_admins(response_text)
            except ApiException:
                return make_response('Error: failed to send notification to admin', 400)

            return make_response('OK', 200)

        @self.__app.route('/notify/telegram/after_first_deposit', methods=['GET'])
        def send_notification_after_first_deposit_use_telegram_bot() -> Response:
            user_id: str = request.args.get('user_id', '', str)
            amount: str = request.args.get('amount', '', str)
            currency: str = request.args.get('currency', '', str)

            if user_id == '' or amount == '' or currency == '':
                return make_response('Bad Request', 400)

            response_text: str = f'User id: {user_id}\n' \
                                 f'Amount: {amount} {currency}'

            try:
                self.__bot.send_notification_to_admins(response_text)
            except ApiException:
                return make_response('Error: failed to send notification to admin', 400)

            return make_response('OK', 200)

        @self.__app.route('/', methods=['POST'])
        def webhook() -> Response:
            if flask.request.headers.get('content-type') != 'application/json':
                return make_response('Error: content-type is not json', 403)

            try:
                json_string: str = flask.request.get_data().decode('utf-8')
                update: Update = Update.de_json(json_string)
                self.__bot.process_new_updates([update])
            except Exception:
                return make_response('Error: failed to process update', 400)

            return make_response('OK', 200)

    def get_app(self) -> Flask:
        return self.__app
