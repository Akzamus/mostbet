from dotenv import load_dotenv
import os
import signal
import json

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEB_HOOK_URL = os.getenv('WEB_HOOK_URL')
MAIN_ADMIN_ID = os.getenv('MAIN_ADMIN_ID')

admin_ids_file = 'admin_ids.json'
admin_ids = []

try:
    with open(admin_ids_file, 'r') as f:
        admin_ids = json.load(f)
except Exception:
    admin_ids.append(int(MAIN_ADMIN_ID))


def save_admin_ids():
    with open(admin_ids_file, 'w') as file:
        json.dump(admin_ids, file)


def handle_exit(signum, frame):
    save_admin_ids()
    exit(0)


signal.signal(signal.SIGTERM, handle_exit)
