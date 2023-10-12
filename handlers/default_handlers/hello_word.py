from loader import bot


@bot.message_handler(content_types=['text'])
def text(message):
    if message.text == 'Привет':
        bot.reply_to(message, f"Привет, {message.from_user.full_name}! Я бот для поиска подходящих билетов."
                              f"Выберите команду, чтобы продолжить")