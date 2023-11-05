Телеграм бот для поиска авиабилетов
=============

![pypi Version](https://pypi-camo.global.ssl.fastly.net/352fd92ae1131f654227ac87897da847005d2d11/68747470733a2f2f696d672e736869656c64732e696f2f707970692f762f707954656c656772616d426f744150492e737667) ![pypipackage Version](https://pypi-camo.global.ssl.fastly.net/d991beaba0f24ebe0e393341e7302b1ec8a075ac/68747470733a2f2f62616467652e667572792e696f2f70792f707974686f6e2d646f74656e762e737667)

# Библиотеки
- requests==2.31.0
- python-dotenv==1.0.0
- peewee==3.16.3
- pyTelegramBotAPI==4.14.0

# Введение
Телеграм бот для поиска авиабилетов - это удобный инструмент, который поможет Вам быстро найти авиабилеты. С помощью бота Вы можете указать место отправления и назначения, а также даты поездки, чтобы получить наилучшие предложения по авиабилетам.

# Использование
Для начала Вам нужно установить виртуальную среду. Инструкция представлена ниже.
```
# заходим в директорию с проектом
C:\Users\admin>cd C:\Users\admin\Desktop\Skillbox ahead\python_basic_diploma

# создаем виртуальное окружение прямо рядом с кодом в директории env
C:\Users\admin\Desktop\Skillbox ahead\python_basic_diploma>python -m venv env

# активируем среду
C:\Users\admin\Desktop\Skillbox ahead\python_basic_diploma>env\Scripts\activate

# для того чтобы установить все пакеты из файла requirements.txt, необходимо выполнить команду:
(env) C:\Users\admin\Desktop\Skillbox ahead\python_basic_diploma>pip install -r requirements.txt
```
Далее заходим в PyCharm. В выборе интерпретатора выбираем "Add New Interpreter" -> "Add Local Interpreter". 
В "Environment" выбираем "Existing" и выбираем наш интерпретатор.

После этого Вам нужно создать файл ".env" и добавить туда необходимые данные.
```
BOT_TOKEN = "Ваш токен для бота, полученный от @BotFather"
API_KEY = "Ваш ключ полученный от API Flight Data"
```

Всего у бота семь команд:
- /start - Запускает бота
- /help - Выводит справку о командах
- /hello_world - Приветствует пользователя
- /low - Находит самый дешёвый билет за год
- /high - Находит самый дорогой день для покупки билета
- /custom - Находит дешёвый билет по Вашим критериям
- /history - Выдаёт историю Ваших запросов (последние десять)


