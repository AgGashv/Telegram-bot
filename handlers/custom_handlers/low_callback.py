from loader import bot
from handlers.custom_handlers.low import low
from telebot import StateMemoryStorage, State
from utils import set_bot_commands


@bot.callback_query_handler(func=lambda call: True)
def low_callback(call):
    if call.data == 'yes':
        low(call.message)
    elif call.data == 'no':
        bot.set_state(call.message.from_user.id, StateMemoryStorage(), call.message.chat.id)
        bot.send_message(call.message.chat.id, set_bot_commands.text)


