from loader import bot


@bot.message_handler(commands=['hello_world'])
def hello_world(message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
