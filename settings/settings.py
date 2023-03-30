from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')
MAIN_ADMIN_ID = int(os.getenv('MAIN_ADMIN_ID'))
DB_PATH = os.getenv('DB_PATH')
