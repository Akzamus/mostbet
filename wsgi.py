from app.telegram_webhook_handler import TelegramWebhookHandler
from app.admin_service import AdminService
from app.telegram_bot import TelegramBot
from config.settings import *

admin_service = AdminService(
    db_path=DB_PATH,
    main_admin_id=MAIN_ADMIN_ID
)

telegram_bot = TelegramBot(
    token=BOT_TOKEN,
    admin_service=admin_service
)

telegram_bot.set_webhook(WEB_HOOK_URL)

telegram_webhook_handler = TelegramWebhookHandler(
    telegram_bot=telegram_bot
)

app = telegram_webhook_handler.get_app()

if __name__ == '__main__':
    app.run()

