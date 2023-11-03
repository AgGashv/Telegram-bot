from telebot.handler_backends import State, StatesGroup


class FlightInfoStateLow(StatesGroup):
    def __init__(self, origin_city: State = State(), destination_city: State = State()):
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
    def __init__(self, origin_city: State = State(), destination_city: State = State()):
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


class FlightInfoStateCustom(FlightInfoStateLow):
    def __init__(self, origin_city: State, destination_city: State, departure_date: State, return_date: State,
                 one_way: bool = True):
        super().__init__(origin_city, destination_city)
        self.__one_way = one_way
        self.__departure_date = departure_date
        self.__return_date = return_date

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

    @property
    def one_way(self):
        return self.__one_way

    @one_way.setter
    def one_way(self, one_way):
        self.__one_way = one_way

    @property
    def departure_date(self):
        return self.__departure_date

    @departure_date.setter
    def departure_date(self, departure_date):
        self.__departure_date = departure_date

    @property
    def return_date(self):
        return self.__return_date

    @return_date.setter
    def return_date(self, return_date):
        self.__return_date = return_date
