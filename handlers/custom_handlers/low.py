from telebot import StateMemoryStorage
from keyboards.inline.low_continue_ask import ask_to_continue_low
from keyboards.inline.aviasales_site import site_button
from database.database import Users
from loader import bot
from states.flight_info import FlightInfoStateLow
from config_data.config import querystring1, direct_url, headers, prices_url
from database.database import Cities
from telebot.types import Message
import requests
import json


@bot.message_handler(commands=['low'])
def low(message: Message) -> None:
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
def get_destination_city(message: Message) -> None:
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
                    if price_data['data'] == {}:
                        ticket_info = '{}{} <b>→</b> {}{}\n\n' \
                                      'Цена: {:,} руб.\n' \
                                      'Дата: {}\n' \
                                      'Информация об авиакомпании и номере рейса отсутствуют.'.format(
                                        Cities[id_origin].flag,
                                        Cities[id_origin].name,
                                        Cities[id_destination].name,
                                        Cities[id_destination].flag,
                                        direct_data_value,
                                        direct_data_date[-2:] + direct_data_date[4:8] + direct_data_date[:4],
                                        ).replace(',', ' ')
                    else:
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

                    bot.send_message(message.chat.id, ticket_info, parse_mode="html", reply_markup=site_button(
                        Cities[id_origin].code,
                        direct_data_date[-2:] + direct_data_date[5:7],
                        Cities[id_destination].code
                    ))

                    first_instance = 0
                    rows_count = 0

                    for i in Users.select().where(Users.id == message.from_user.id):
                        rows_count += 1
                        if rows_count == 1:
                            first_instance = i

                    if rows_count == 10:
                        first = Users.delete().where(Users.history_date == first_instance.history_date)
                        first.execute()

                    user = Users.create(id=message.from_user.id, history_command='/low',
                                        history_info='{}{} <b>→</b> {}{} Цена: {} руб.\n'.format(
                                            Cities[id_origin].flag,
                                            Cities[id_origin].name,
                                            Cities[id_destination].name,
                                            Cities[id_destination].flag,
                                            direct_data_value
                                        ))
                    user.save()
                else:
                    bot.send_message(message.from_user.id, "Что-то пошло не по плану. Повторите попытку позже. "
                                                           "Извините за доставленные неудобства.")
        else:
            bot.send_message(message.from_user.id, "Что-то пошло не по плану. Повторите попытку позже. "
                                                   "Извините за доставленные неудобства.")

        bot.set_state(message.from_user.id, StateMemoryStorage(), message.chat.id)

        bot.send_message(message.from_user.id, "Хотите продолжить?", reply_markup=ask_to_continue_low())
