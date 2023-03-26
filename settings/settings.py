from dotenv import load_dotenv
import threading
import json
import os

load_dotenv()
lock = threading.Lock()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')
MAIN_ADMIN_ID = int(os.getenv('MAIN_ADMIN_ID'))

admin_ids_file = 'admin_ids.json'
admin_ids = []


def save_admin_ids():
    with open(admin_ids_file, 'w') as file:
        json.dump(admin_ids, file)


try:
    with open(admin_ids_file, 'r') as f:
        admin_ids = json.load(f)
except Exception:
    with lock:
        admin_ids.append(MAIN_ADMIN_ID)
        save_admin_ids()

