import telebot

from settings.settings import MAIN_ADMIN_ID


class TelegramBot:
    def __init__(self, token, url, admin_service):
        self.admin_service = admin_service
        self.bot = telebot.TeleBot(token=token)
        self.bot.set_webhook(url=url)

        @self.bot.message_handler(commands=['start'])
        def get_response_to_start_command(message):
            response_text = '''
            Commands:
            /add (user_id) - add admin
            /delete (user_id) - delete admin
            /check - check your role 
            '''
            self.bot.send_message(message.chat.id, response_text)

        @self.bot.message_handler(commands=['check'])
        def check_role(message):
            user_id = message.from_user.id
            response_text = 'You are not an admin'
            if user_id == MAIN_ADMIN_ID:
                response_text = 'You are an main admin'
            elif self.admin_service.is_admin(user_id):
                response_text = 'You are an admin'
            self.bot.send_message(user_id, response_text)

        @self.bot.message_handler(commands=['add'])
        def add_admin(message):
            admin_ids = self.admin_service.get_admin_ids()
            user_id = message.from_user.id

            if not self.admin_service.is_admin(user_id):
                self.bot.send_message(user_id, 'You are not an admin')
                return

            command_parts = message.text.split(' ')

            if len(command_parts) != 2:
                self.bot.send_message(user_id, 'Please specify the user ID')
                return

            if not command_parts[1].isdigit():
                self.bot.send_message(user_id, 'The user ID should consist only of digits')
                return

            new_admin_id = int(command_parts[1])

            if not self.check_user_existence(new_admin_id):
                self.bot.send_message(user_id, 'The user does not exists')
                return

            if new_admin_id in admin_ids or new_admin_id == MAIN_ADMIN_ID:
                self.bot.send_message(user_id, 'The user is already an admin')
                return

            self.admin_service.add_admin(new_admin_id)
            self.bot.send_message(user_id, 'User added to admins')
            self.bot.send_message(new_admin_id, 'Now you are an admin')

        @self.bot.message_handler(commands=['delete'])
        def delete_admin(message):
            user_id = message.from_user.id

            if user_id != MAIN_ADMIN_ID:
                self.bot.send_message(user_id, 'You are not a main admin')
                return

            command_parts = message.text.split(' ')

            if len(command_parts) != 2:
                self.bot.send_message(user_id, 'Please specify the user ID')
                return

            if not command_parts[1].isdigit():
                self.bot.send_message(user_id, 'The user ID should consist only of digits')
                return

            admin_id = int(command_parts[1])

            if admin_id == MAIN_ADMIN_ID:
                self.bot.send_message(user_id, 'You cannot delete yourself from the list')
                return

            if not self.admin_service.is_admin(admin_id):
                self.bot.send_message(user_id, 'The admin with this id was not found in the list')
                return

            self.admin_service.remove_admin(admin_id)
            self.bot.send_message(user_id, 'Admin removed')

    def send_notification_to_admins(self, text):
        admin_ids = self.admin_service.get_admin_ids()
        for admin_id in admin_ids:
            self.bot.send_message(admin_id, text)

    def check_user_existence(self, user_id):
        user_exists = True
        try:
            self.bot.send_message(user_id, '')
        except telebot.apihelper.ApiException:
            user_exists = False
        return user_exists

