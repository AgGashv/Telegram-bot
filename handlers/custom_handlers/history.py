from database.database import Users
from loader import bot


@bot.message_handler(commands=['history'])
def get_history(message):
    text = ''
    for i, user in enumerate(Users.select().where(Users.id == message.from_user.id)):
        text += '{}. Команда: {}\nЧто искали: {}Дата и время: {}\n\n'.format(
            i + 1,
            user.history_command,
            user.history_info,
            user.history_date
        )

    if text == '':
        bot.send_message(message.from_user.id, 'Список истории запросов пуст.')
    else:
        bot.send_message(message.from_user.id, text, parse_mode="html")
