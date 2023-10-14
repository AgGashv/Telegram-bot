from telebot.types import BotCommand
from config_data.config import DEFAULT_COMMANDS


def set_default_commands(bot):
    bot.set_my_commands(
        [BotCommand(*i) for i in DEFAULT_COMMANDS]
    )


text = ''
for element in DEFAULT_COMMANDS:
    text += '/' + ' - '.join(element) + '\n'


