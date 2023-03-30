from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
MAIN_ADMIN_ID = int(os.getenv('MAIN_ADMIN_ID'))

