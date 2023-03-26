from dotenv import load_dotenv
import os
import atexit
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


atexit.register(lambda: json.dump(admin_ids, open(f'./settings/{admin_ids_file}', 'w')))
