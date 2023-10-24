from telebot.handler_backends import State, StatesGroup


class FlightInfoStateLow(StatesGroup):
    def __init__(self, origin_city=State(), destination_city=State()):
        self.__origin_city = origin_city
        self.__destination_city = destination_city

    @property
    def origin_city(self):
        return self.__origin_city

    @origin_city.setter
    def origin_city(self, origin_city):
        self.__origin_city = origin_city

    @property
    def destination_city(self):
        return self.__destination_city

    @destination_city.setter
    def destination_city(self, destination_city):
        self.__destination_city = destination_city


class FlightInfoStateHigh(FlightInfoStateLow):
    def __init__(self, origin_city=State(), destination_city=State()):
        super().__init__(origin_city, destination_city)

    @property
    def origin_city(self):
        return self.__origin_city

    @origin_city.setter
    def origin_city(self, origin_city):
        self.__origin_city = origin_city

    @property
    def destination_city(self):
        return self.__destination_city

    @destination_city.setter
    def destination_city(self, destination_city):
        self.__destination_city = destination_city
