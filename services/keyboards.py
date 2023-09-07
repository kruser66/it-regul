from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)


def start_keyboard():
    start_keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Для работы с ботом необходимо принять согласие'
    )
    button_apply = KeyboardButton('Принять', request_contact=True)
    button_exit = KeyboardButton('Выход')

    start_keyboard.add(button_apply, button_exit, row_width=1)

    return start_keyboard


def change_user_keyboard():
    return InlineKeyboardMarkup(
        keyboard=[
            [InlineKeyboardButton('Изменить имя', callback_data='change_firstname')],
            [InlineKeyboardButton('Изменить фамилию', callback_data='change_lastname')],
            [InlineKeyboardButton('Заменить телефон', callback_data='change_phone')],
        ]
    )
