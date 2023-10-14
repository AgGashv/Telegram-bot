import peewee

db = peewee.SqliteDatabase(database="database/database.db")


class Cities(peewee.Model):
    name = peewee.CharField()
    code = peewee.CharField()
    flag = peewee.CharField()

    class Meta:
        database = db
