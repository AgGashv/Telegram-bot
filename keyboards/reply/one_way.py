from telebot.types import ReplyKeyboardMarkup


def ask_to_one_way_attribute():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('В одну сторону', 'Туда-обратно')
    return markup
