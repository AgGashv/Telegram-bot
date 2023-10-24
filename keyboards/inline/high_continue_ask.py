from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def ask_to_continue_high():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Да', callback_data='yes_high'),
               InlineKeyboardButton('Нет', callback_data='no'))
    return markup
