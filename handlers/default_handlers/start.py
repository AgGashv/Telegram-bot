from telebot.types import Message

from loader import bot
from config_data.config import DEFAULT_COMMANDS


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    text = f"Привет, {message.from_user.full_name}! Я бот для поиска подходящих билетов. " \
           f"Выберите команду:\n"
    for command, desk in DEFAULT_COMMANDS:
        text += f'/{command} - {desk}\n'
    bot.reply_to(message, text)
