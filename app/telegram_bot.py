import time

import telebot

from app.admin_service import AdminService
from telebot import TeleBot
from telebot.types import Message, Update
from typing import List


class TelegramBot:
    def __init__(self, token: str, url: str, admin_service: AdminService) -> None:
        self.__admin_service: AdminService = admin_service
        self.__bot: TeleBot = TeleBot(token=token)
        time.sleep(0.1)
        self.__bot.set_webhook(url=url)

        @self.__bot.message_handler(commands=['start'])
        def get_response_to_start_command(message: Message) -> None:
            response_text = '''
            Commands:
            /add (user_id) - add admin
            /delete (user_id) - delete admin
            /check - check your role 
            '''
            self.__bot.send_message(message.chat.id, response_text)

        @self.__bot.message_handler(commands=['check'])
        def check_role(message: Message) -> None:
            user_id: int = message.from_user.id
            response_text: str = 'You are not an admin'
            if user_id == self.__admin_service.get_main_admin_id():
                response_text = 'You are an main admin'
            elif self.__admin_service.is_admin(user_id):
                response_text = 'You are an admin'
            self.__bot.send_message(user_id, response_text)

        @self.__bot.message_handler(commands=['add'])
        def add_admin(message: Message) -> None:
            admin_ids: List[int] = self.__admin_service.get_admin_ids()
            user_id: int = message.from_user.id

            if not self.__admin_service.is_admin(user_id):
                self.__bot.send_message(user_id, 'You are not an admin')
                return

            command_parts: List[str] = message.text.split(' ')

            if len(command_parts) != 2:
                self.__bot.send_message(user_id, 'Please specify the user ID')
                return

            if not command_parts[1].isdigit():
                self.__bot.send_message(user_id, 'The user ID should consist only of digits')
                return

            new_admin_id: int = int(command_parts[1])

            if not self.check_user_existence(new_admin_id):
                self.__bot.send_message(user_id, 'The user does not exists')
                return

            if new_admin_id in admin_ids or new_admin_id == self.__admin_service.get_main_admin_id():
                self.__bot.send_message(user_id, 'The user is already an admin')
                return

            self.__admin_service.add_admin(new_admin_id)
            self.__bot.send_message(user_id, 'User added to admins')
            self.__bot.send_message(new_admin_id, 'Now you are an admin')

        @self.__bot.message_handler(commands=['delete'])
        def delete_admin(message: Message) -> None:
            main_admin_id: int = self.__admin_service.get_main_admin_id()
            user_id: int = message.from_user.id

            if user_id != main_admin_id:
                self.__bot.send_message(user_id, 'You are not a main admin')
                return

            command_parts: List[str] = message.text.split(' ')

            if len(command_parts) != 2:
                self.__bot.send_message(user_id, 'Please specify the user ID')
                return

            if not command_parts[1].isdigit():
                self.__bot.send_message(user_id, 'The user ID should consist only of digits')
                return

            admin_id: int = int(command_parts[1])

            if admin_id == main_admin_id:
                self.__bot.send_message(user_id, 'You cannot delete yourself from the list')
                return

            if not self.__admin_service.is_admin(admin_id):
                self.__bot.send_message(user_id, 'The admin with this id was not found in the list')
                return

            self.__admin_service.remove_admin(admin_id)
            self.__bot.send_message(user_id, 'Admin removed')

    def send_notification_to_admins(self, text: str) -> None:
        admin_ids: List[int] = self.__admin_service.get_admin_ids()
        for admin_id in admin_ids:
            self.__bot.send_message(admin_id, text)

    def check_user_existence(self, user_id: int) -> bool:
        user_exists: bool = True
        try:
            self.__bot.send_message(user_id, '')
        except telebot.apihelper.ApiException:
            user_exists = False
        return user_exists

    def process_new_updates(self, updates: List[Update]) -> None:
        self.__bot.process_new_updates(updates)
