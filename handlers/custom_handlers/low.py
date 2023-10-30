from keyboards.inline.low_continue_ask import ask_to_continue_low
from loader import bot
from states.flight_info import FlightInfoStateLow
from config_data.config import querystring1, direct_url, headers, prices_url
from database.database import Cities
import requests
import json


@bot.message_handler(commands=['low'])
def low(message):
    bot.set_state(message.chat.id, FlightInfoStateLow.origin_city, message.chat.id)
    bot.send_message(message.chat.id, "Введите город отправления.")


@bot.message_handler(state=FlightInfoStateLow.origin_city)
def get_origin_city(message):
    try:
        Cities.get(Cities.name == message.text.title())
    except Exception:
        bot.send_message(message.from_user.id, "Неправильный ввод. Город не найден.")
    else:
        bot.set_state(message.from_user.id, FlightInfoStateLow.destination_city, message.chat.id)
        bot.send_message(message.from_user.id, "Введите город прибытия.")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['origin_city'] = message.text.title()


@bot.message_handler(state=FlightInfoStateLow.destination_city)
def get_destination_city(message):
    try:
        Cities.get(Cities.name == message.text.title())
    except Exception:
        bot.send_message(message.from_user.id, "Неправильный ввод. Город не найден.")
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['destination_city'] = message.text.title()

        id_origin = Cities.get(Cities.name == data['origin_city'])
        id_destination = Cities.get(Cities.name == data['destination_city'])

        querystring1.update({"origin": Cities[id_origin].code,
                            "destination": Cities[id_destination].code})

        response = requests.request("GET", direct_url, headers=headers,
                                    params=querystring1, timeout=20)

        if response.status_code == requests.codes.ok:
            direct_data = json.loads(response.text)
            try:
                direct_data_value = direct_data['data'][0].get('value')
                direct_data_date = direct_data['data'][0].get('depart_date')
            except IndexError:
                bot.send_message(message.from_user.id, "Билеты не найдены. Попробуйте другие города.")
            else:
                response1 = requests.request("GET", prices_url, headers=headers,
                                             params={"origin": Cities[id_origin].code,
                                                     "destination": Cities[id_destination].code,
                                                     "departure_date": direct_data_date,
                                                     "calendar_type": "departure_date"},
                                             timeout=20)

                if response1.status_code == requests.codes.ok:
                    price_data = json.loads(response1.text)
                    ticket_info = '{}{} <b>→</b> {}{}\n\n' \
                                  'Цена: {:,} руб.\n' \
                                  'Дата: {}\n' \
                                  'Авиакомпания: {}\n' \
                                  'Номер рейса: {}'.format(
                                    Cities[id_origin].flag,
                                    Cities[id_origin].name,
                                    Cities[id_destination].name,
                                    Cities[id_destination].flag,
                                    direct_data_value,
                                    direct_data_date[-2:] + direct_data_date[4:8] + direct_data_date[:4],
                                    price_data['data'].get(direct_data_date).get('airline'),
                                    price_data['data'].get(direct_data_date).get('flight_number')
                                    ).replace(',', ' ')
                    bot.send_message(message.chat.id, ticket_info, parse_mode="html")
                else:
                    bot.send_message(message.from_user.id, "Что-то пошло не по плану. Повторите попытку позже. "
                                                           "Извините за доставленные неудобства.")
        else:
            bot.send_message(message.from_user.id, "Что-то пошло не по плану. Повторите попытку позже. "
                                                   "Извините за доставленные неудобства.")

        bot.send_message(message.from_user.id, "Хотите продолжить?", reply_markup=ask_to_continue_low())

