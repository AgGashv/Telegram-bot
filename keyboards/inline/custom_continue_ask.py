from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def ask_to_continue_custom():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data='yes_custom'),
               InlineKeyboardButton('Нет', callback_data='no'))
    return markup
