from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def site_button(origin_code, depart_day_month, destination_code, return_day_month=''):
    markup = InlineKeyboardMarkup()
    url = 'https://www.aviasales.ru/search/' + origin_code + \
          depart_day_month + destination_code + return_day_month + '1'
    markup.add(InlineKeyboardButton('Посмотреть билеты', url=url))
    return markup
