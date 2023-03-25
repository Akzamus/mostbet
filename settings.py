from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')
USER_ID = os.getenv('USER_ID')
