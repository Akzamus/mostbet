from settings.settings import WEB_HOOK_URL, APP_HOST, APP_PORT
from telegram_bot import bot
from app import app

import time

if __name__ == '__main__':
    bot.remove_webhook()
    time.sleep(0.1)

    bot.set_webhook(url=WEB_HOOK_URL)
    app.run(host=APP_HOST, port=APP_PORT)