import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_KEY = os.getenv("API_KEY")

headers = {'x-access-token': API_KEY}

prices_url = "https://api.travelpayouts.com/v1/prices/calendar"
direct_url = "https://api.travelpayouts.com/v2/prices/latest"
custom_url = "https://api.travelpayouts.com/v1/prices/direct"

querystring1 = {"one_way": True, "period_type": "year", "sorting": "price",
                "show_to_affiliates": True, 'limit': 1000}

DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("hello_world", "Приветствие"),
    ("low", "Найти самый дешёвый билет"),
    ("high", "Найти самый дорогой билет среди дешёвых"),
    ("custom", "Найти дешёвый билет по вашим критериям"),
    ("history", "История запросов (последние десять)")
)
