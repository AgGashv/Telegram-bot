from telebot.types import ReplyKeyboardMarkup


def ask_to_one_way_attribute() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('В одну сторону', 'Туда-обратно')
    return markup
