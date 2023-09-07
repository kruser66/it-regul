import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from telebot import TeleBot, custom_filters
from telebot.types import ReplyKeyboardRemove
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

from config.settings import BOT_TOKEN
from services.messages import welcome_message, user_info
from services.keyboards import start_keyboard, change_user_keyboard, apply_user_keyboard
from services import db


state_storage = StateMemoryStorage()
bot = TeleBot(BOT_TOKEN, state_storage=state_storage)


class UserStates(StatesGroup):
    user_firstname = State()
    user_lastname = State()


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):

    user = db.get_user(message.from_user.id)

    if user:
        bot.send_message(
            chat_id=message.chat.id,
            text=user_info(user),
            reply_markup=change_user_keyboard()
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text=welcome_message(),
            reply_markup=start_keyboard()
        )


@bot.message_handler(func=lambda message: message.text == 'Выход')
@bot.message_handler(commands=['cancel'])
def send_bye(message):

    bot.send_message(
        chat_id=message.chat.id,
        text='До свидания',
        reply_markup=ReplyKeyboardRemove()
    )


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    chat_id = message.chat.id
    if message.contact is not None:
        print(message.contact)
        bot.set_state(user_id=chat_id, state=UserStates.user_firstname)
        bot.add_data(
            chat_id,
            chat_id,
            phone=message.contact.phone_number,
            username=message.chat.username
        )

        bot.send_message(
            chat_id=chat_id,
            text='Введите имя:'
        )


@bot.message_handler(state=UserStates.user_firstname)
def get_user_firstname(message):
    chat_id = message.chat.id
    bot.set_state(user_id=chat_id, state=UserStates.user_lastname)
    bot.add_data(chat_id, chat_id, firstname=message.text)

    bot.send_message(
        chat_id=chat_id,
        text='Введите фамилию:'
    )


@bot.message_handler(state=UserStates.user_lastname)
def check_user_data(message):
    chat_id = message.chat.id
    bot.add_data(chat_id, chat_id, lastname=message.text)

    with bot.retrieve_data(chat_id, chat_id) as data:
        user = db.update_or_create_user(
            telegram_id=chat_id,
            **data
        )

    bot.send_message(
        chat_id=chat_id,
        text=user_info(user),
        reply_markup=change_user_keyboard()
    )
    bot.delete_state(chat_id, chat_id)


bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.infinity_polling()
