from loader import bot
from handlers.custom_handlers.low import low
from handlers.custom_handlers.high import high
from handlers.custom_handlers.custom import custom
from telebot import StateMemoryStorage
from utils import set_bot_commands


@bot.callback_query_handler(func=lambda call: True)
def low_callback(call):
    if call.data == 'yes_low':
        low(call.message)
    elif call.data == 'yes_high':
        high(call.message)
    elif call.data == 'yes_custom':
        custom(call.message)
    elif call.data == 'no':
        bot.set_state(call.message.from_user.id, StateMemoryStorage(), call.message.chat.id)
        bot.send_message(call.message.chat.id, f'Выберите команду:\n{set_bot_commands.text}')


