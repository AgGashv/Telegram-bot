from telebot import StateMemoryStorage
from telebot.types import ReplyKeyboardRemove
from database.database import Users
from keyboards.inline.custom_continue_ask import ask_to_continue_custom
from keyboards.inline.aviasales_site import site_button
from keyboards.reply.one_way import ask_to_one_way_attribute
from loader import bot
from states.flight_info import FlightInfoStateCustom
from config_data.config import querystring1, direct_url, headers, prices_url, custom_url
from database.database import Cities
from telebot.types import Message
import requests
import json
import re
import datetime


@bot.message_handler(commands=['custom'])
def custom(message: Message) -> None:
    bot.set_state(message.chat.id, FlightInfoStateCustom.origin_city, message.chat.id)
    bot.send_message(message.chat.id, "Введите город отправления.", )


@bot.message_handler(state=FlightInfoStateCustom.origin_city)
def get_origin_city(message: Message) -> None:
    try:
        Cities.get(Cities.name == message.text.title())
    except Exception:
        bot.send_message(message.from_user.id, "Неправильный ввод. Город не найден.")
    else:
        bot.set_state(message.from_user.id, FlightInfoStateCustom.destination_city, message.chat.id)
        bot.send_message(message.from_user.id, "Введите город прибытия.")

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['origin_city'] = message.text.title()


@bot.message_handler(state=FlightInfoStateCustom.destination_city)
def get_destination_city(message: Message) -> None:
    try:
        Cities.get(Cities.name == message.text.title())
    except Exception:
        bot.send_message(message.from_user.id, "Неправильный ввод. Город не найден.")
    else:
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['destination_city'] = message.text.title()

        bot.set_state(message.from_user.id, FlightInfoStateCustom.one_way, message.chat.id)
        bot.send_message(message.from_user.id, 'Выберите "Туда-обратно" или "В одну сторону"',
                         reply_markup=ask_to_one_way_attribute())


@bot.message_handler(state=FlightInfoStateCustom.one_way)
def get_one_way_attribute(message: Message) -> None:
    if message.text == 'Туда-обратно' or message.text == 'В одну сторону':
        if message.text == 'Туда-обратно':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['one_way'] = False
        elif message.text == 'В одну сторону':
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['one_way'] = True

        bot.set_state(message.from_user.id, FlightInfoStateCustom.departure_date, message.chat.id)
        bot.send_message(message.from_user.id, "Введите дату отправления в формате: дд-мм-гг. Пример: 01-01-2023",
                         reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.from_user.id, 'Неправильный ввод. Выберите один из представленных '
                                               'вариантов.', reply_markup=ask_to_one_way_attribute())


@bot.message_handler(state=FlightInfoStateCustom.departure_date)
def get_departure_date(message: Message) -> None:
    if re.search(r'\b\d{2}-\d{2}-\d{4}\b', message.text):
        try:
            date = datetime.date(int(message.text[6:]), int(message.text[3:5]), int(message.text[0:2]))
            if date < datetime.date.today():
                raise ValueError
        except ValueError:
            bot.send_message(message.from_user.id, 'Дата не актуальна. Введите другую дату.')
        except Exception:
            bot.send_message(message.from_user.id, 'Неправильный ввод. Введите дату отправления в формате: дд-мм-гг')
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['departure_date'] = date

            id_origin = Cities.get(Cities.name == data['origin_city'])
            id_destination = Cities.get(Cities.name == data['destination_city'])

            if data['one_way']:
                querystring1.update({"origin": Cities[id_origin].code,
                                     "destination": Cities[id_destination].code})

                response = requests.request("GET", direct_url, headers=headers,
                                            params=querystring1, timeout=20)

                if response.status_code == requests.codes.ok:
                    direct_data = json.loads(response.text)
                    direct_data_value = ''
                    direct_data_date = data['departure_date'].isoformat()

                    for info in direct_data['data']:
                        if info['depart_date'] == direct_data_date:
                            direct_data_value = info['value']

                    response1 = requests.request("GET", prices_url, headers=headers,
                                                 params={"origin": Cities[id_origin].code,
                                                         "destination": Cities[id_destination].code,
                                                         "departure_date": direct_data_date,
                                                         "calendar_type": "departure_date"},
                                                 timeout=20)

                    if response1.status_code == requests.codes.ok:
                        price_data = json.loads(response1.text)
                        try:
                            airline = price_data['data'].get(direct_data_date).get('airline')
                            flight_number = price_data['data'].get(direct_data_date).get('flight_number')
                        except Exception:
                            bot.send_message(message.from_user.id, "Билеты не найдены. Попробуйте другие города.")
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
                                            airline,
                                            flight_number
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

                            user = Users.create(id=message.from_user.id, history_command='/custom',
                                                history_info='{}{} <b>→</b> {}{} Цена: {} руб.\n'.format(
                                                    Cities[id_origin].flag,
                                                    Cities[id_origin].name,
                                                    Cities[id_destination].name,
                                                    Cities[id_destination].flag,
                                                    direct_data_value
                                                ))
                            user.save()
                            bot.set_state(message.from_user.id, StateMemoryStorage(), message.chat.id)
                    else:
                        bot.send_message(message.from_user.id, "Что-то пошло не по плану. Повторите попытку позже. "
                                                               "Извините за доставленные неудобства.")

                bot.set_state(message.from_user.id, StateMemoryStorage(), message.chat.id)

                bot.send_message(message.from_user.id, "Хотите продолжить?", reply_markup=ask_to_continue_custom())

            else:
                bot.set_state(message.from_user.id, FlightInfoStateCustom.return_date, message.chat.id)
                bot.send_message(message.from_user.id, "Введите дату возвращения в формате: дд-мм-гг. "
                                                       "Пример: 01-01-2023",
                                 reply_markup=ReplyKeyboardRemove())

    else:
        bot.send_message(message.from_user.id, 'Неправильный ввод. Введите дату отправления в формате: дд-мм-гг')


@bot.message_handler(state=FlightInfoStateCustom.return_date)
def get_return_date(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        id_origin = Cities.get(Cities.name == data['origin_city'])
        id_destination = Cities.get(Cities.name == data['destination_city'])

    if re.search(r'\b\d{2}-\d{2}-\d{4}\b', message.text):
        try:
            date = datetime.date(int(message.text[6:]), int(message.text[3:5]), int(message.text[0:2]))
            date_difference = date - data['departure_date']

            if date < data['departure_date']:
                raise IndexError

            if date_difference.days > 30:
                raise ValueError

        except ValueError:
            bot.send_message(message.from_user.id, "Разница в датах не должна превышать 30 дней.")
        except IndexError:
            bot.send_message(message.from_user.id, 'Неправильный ввод. Дата возвращения раньше даты отправления.')
        except Exception:
            bot.send_message(message.from_user.id, 'Неправильный ввод. Введите дату возвращения в формате: дд-мм-гг')
        else:
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['return_date'] = date

            query = {"origin": Cities[id_origin].code,
                     "destination": Cities[id_destination].code,
                     "depart_date": data['departure_date'].isoformat(),
                     "return_date": data['return_date'].isoformat()
                     }
            resp = requests.request("GET", custom_url, headers=headers,
                                    params=query, timeout=20)

            if resp.status_code == requests.codes.ok:
                direct_data = json.loads(resp.text)
                try:
                    direct_data_price = direct_data['data'].get(Cities[id_destination].code).get('0').get('price')
                    direct_data_airline = direct_data['data'].get(Cities[id_destination].code).get('0').get('airline')
                    direct_data_flight_number = direct_data['data'].get(Cities[id_destination].code).get('0').get(
                        'flight_number')
                except Exception:
                    bot.send_message(message.from_user.id, "Билеты не найдены. Попробуйте другие города.")
                else:
                    direct_data_depart_date = data['departure_date'].isoformat()
                    direct_data_return_date = data['return_date'].isoformat()
                    ticket_info = '{}{} <b>⟷</b> {}{}\n\n' \
                                  'Цена: {:,} руб.\n' \
                                  'Дата отправления: {}\n' \
                                  'Дата возвращения: {}\n' \
                                  'Авиакомпания: {}\n' \
                                  'Номер рейса: {}'.format(
                                    Cities[id_origin].flag,
                                    Cities[id_origin].name,
                                    Cities[id_destination].name,
                                    Cities[id_destination].flag,
                                    direct_data_price,
                                    direct_data_depart_date[-2:] + direct_data_depart_date[4:8]
                                    + direct_data_depart_date[:4],
                                    direct_data_return_date[-2:] + direct_data_return_date[4:8]
                                    + direct_data_return_date[:4],
                                    direct_data_airline,
                                    direct_data_flight_number
                                    ).replace(',', ' ')

                    bot.send_message(message.chat.id, ticket_info, parse_mode="html", reply_markup=site_button(
                        Cities[id_origin].code,
                        direct_data_depart_date[-2:] + direct_data_depart_date[5:7],
                        Cities[id_destination].code,
                        direct_data_return_date[-2:] + direct_data_return_date[5:7]
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

                    user = Users.create(id=message.from_user.id, history_command='/custom',
                                        history_info='{}{} <b>⟷</b> {}{} Цена: {} руб.\n'.format(
                                            Cities[id_origin].flag,
                                            Cities[id_origin].name,
                                            Cities[id_destination].name,
                                            Cities[id_destination].flag,
                                            direct_data_price
                                        ))
                    user.save()
                    bot.set_state(message.from_user.id, StateMemoryStorage(), message.chat.id)
            else:
                bot.send_message(message.from_user.id, "Что-то пошло не по плану. Повторите попытку позже. "
                                                       "Извините за доставленные неудобства.")

            bot.set_state(message.from_user.id, StateMemoryStorage(), message.chat.id)

            bot.send_message(message.from_user.id, "Хотите продолжить?", reply_markup=ask_to_continue_custom())
    else:
        bot.send_message(message.from_user.id, 'Неправильный ввод. Введите дату отправления в формате: дд-мм-гг')


