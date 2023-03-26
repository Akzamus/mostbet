from settings.settings import BOT_TOKEN, admin_ids, MAIN_ADMIN_ID
import telebot

bot = telebot.TeleBot(token=BOT_TOKEN)


def send_notification_to_admins(text):
    for admin_id in admin_ids:
        bot.send_message(admin_id, text)


def check_user_existence(user_id):
    user_exists = True
    try:
        bot.send_message(user_id, 'Now you are an admin')
    except telebot.apihelper.ApiException:
        user_exists = False
    return user_exists


@bot.message_handler(commands=['start'])
def get_response_to_start_command(message):
    response_text = '''
    Commands:
    /add (user_id) - add admin
    /delete (user_id) - delete admin
    /check - check your role 
    '''
    bot.send_message(message.chat.id, response_text)


@bot.message_handler(commands=['check'])
def check_role(message):
    user_id = message.from_user.id
    response_text = 'You are not an admin'
    if user_id == MAIN_ADMIN_ID:
        response_text = 'You are a main admin'
    elif user_id in admin_ids:
        response_text = 'You are an admin'
    bot.send_message(user_id, response_text)


@bot.message_handler(commands=['add'])
def add_admin(message):
    user_id = message.from_user.id
    response_text = 'You are not an admin'
    if user_id in admin_ids:
        words = message.text.split()
        if len(words) != 2:
            response_text = 'Incorrect input, correct input format:\n' \
                            '/add (user_id)'
        elif not words[1].isdigit():
            response_text = 'The user id consists only of digits'
        elif check_user_existence(int(words[1])):
            if int(words[1]) in admin_ids:
                response_text = 'The user is already an admin'
            else:
                admin_ids.append(int(words[1]))
                response_text = 'User added to admins'
        else:
            response_text = 'The user with this id does not exists or ' \
                            'the chat with the bot has not started'
    bot.send_message(user_id, response_text)


@bot.message_handler(commands=['delete'])
def delete_admin(message):
    user_id = message.from_user.id
    response_text = 'You are not a main admin'
    if user_id == int(MAIN_ADMIN_ID):
        words = message.text.split()
        if len(words) != 2:
            response_text = 'Incorrect input, correct input format:\n' \
                            '/delete (user_id)'
        elif not words[1].isdigit():
            response_text = 'The user id consists only of digits'
        elif int(words[1]) in admin_ids:
            if int(words[1]) == int(MAIN_ADMIN_ID):
                response_text = 'You cannot delete yourself from the list'
            else:
                admin_ids.remove(int(words[1]))
                response_text = 'Admin removed from the list'
        else:
            response_text = 'The admin with this id was not found in the list'
    bot.send_message(user_id, response_text)
