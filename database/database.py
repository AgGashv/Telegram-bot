import peewee
import datetime
from config_data.config import cities_url, headers
import requests
import json

db = peewee.SqliteDatabase(database='database/database.db')

db.connect()


class Cities(peewee.Model):
    name = peewee.CharField()
    code = peewee.CharField()
    flag = peewee.CharField()

    class Meta:
        database = db


class Users(peewee.Model):
    id = peewee.IntegerField()
    history_command = peewee.CharField()
    history_info = peewee.CharField()
    history_date = peewee.DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


flag_list = {'A': '\U0001F1E6', 'B': '\U0001F1E7', 'C': '\U0001F1E8', 'D': '\U0001F1E9', 'E': '\U0001F1EA',
             'F': '\U0001F1EB', 'G': '\U0001F1EC', 'H': '\U0001F1ED', 'I': '\U0001F1EE', 'J': '\U0001F1EF',
             'K': '\U0001F1F0', 'L': '\U0001F1F1', 'M': '\U0001F1F2', 'N': '\U0001F1F3', 'O': '\U0001F1F4',
             'P': '\U0001F1F5', 'Q': '\U0001F1F6', 'R': '\U0001F1F7', 'S': '\U0001F1F8', 'T': '\U0001F1F9',
             'U': '\U0001F1FA', 'V': '\U0001F1FB', 'W': '\U0001F1FC', 'X': '\U0001F1FD', 'Y': '\U0001F1FE',
             'Z': '\U0001F1FF'}


if not (db.table_exists('cities') and db.table_exists('users')):
    Cities.create_table('cities')
    Users.create_table('users')

    response = requests.request("GET", cities_url, headers=headers)
    data = json.loads(response.text)

    for i in data:
        country_code = i.get('country_code')
        flag = ''
        for letter in country_code:
            flag += flag_list.get(letter)
        try:
            city = Cities(name=i.get('name'), code=i.get('code'), flag=flag)
            city.save()
        except Exception:
            pass
