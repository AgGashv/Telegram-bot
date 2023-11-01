import peewee
import datetime

db = peewee.SqliteDatabase(database="database/database.db")


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
