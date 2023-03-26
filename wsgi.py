from settings.settings import WEB_HOOK_URL
from telegram_bot import bot
from app import app

import time

if __name__ == '__main__':
    bot.remove_webhook()
    time.sleep(0.1)

    bot.set_webhook(url=WEB_HOOK_URL)
    app.run()
