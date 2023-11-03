from loader import bot
from handlers.custom_handlers.low import low
from handlers.custom_handlers.high import high
from handlers.custom_handlers.custom import custom
from telebot import StateMemoryStorage
from utils import set_bot_commands
from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda call: True)
def low_callback(call: CallbackQuery) -> None:
    if call.data == 'yes_low':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        low(call.message)
    elif call.data == 'yes_high':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        high(call.message)
    elif call.data == 'yes_custom':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        custom(call.message)
    elif call.data == 'no':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.from_user.id, StateMemoryStorage(), call.message.chat.id)
        bot.send_message(call.message.chat.id, f'Выберите команду:\n{set_bot_commands.text}')


