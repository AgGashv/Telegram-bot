from telebot.handler_backends import State, StatesGroup


class FlightInfoState(StatesGroup):
    origin_city = State()
    destination_city = State()
    flight_info = State()
