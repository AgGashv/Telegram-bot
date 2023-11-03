from loader import bot
from telebot.types import Message


@bot.message_handler(commands=['hello_world'])
def hello_world(message: Message) -> None:
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!")
