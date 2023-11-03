from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def ask_to_continue_low() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data='yes_low'), InlineKeyboardButton('Нет', callback_data='no'))
    return markup
