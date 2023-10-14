from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def ask_to_continue():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data='yes'), InlineKeyboardButton('Нет', callback_data='no'))
    return markup
