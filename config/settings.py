from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN: str = os.getenv('BOT_TOKEN')
WEB_HOOK_URL: str = os.getenv('WEB_HOOK_URL')
MAIN_ADMIN_ID: int = int(os.getenv('MAIN_ADMIN_ID'))
DB_PATH: str = os.getenv('DB_PATH')
