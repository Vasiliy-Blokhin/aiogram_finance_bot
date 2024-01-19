from os import getenv
import sys

from dotenv import load_dotenv
import logging


handler = logging.StreamHandler(sys.stdout)
formater = logging.Formatter(
    '%(name)s, %(funcName)s, %(asctime)s, %(levelname)s - %(message)s.'
)
handler.setFormatter(formater)

load_dotenv()

TOKEN = getenv('BOT_TOKEN')

# IMOEX данные
IMOEX_URL = (
    'http://iss.moex.com/iss/engines/stock/markets/shares/'
    'securities.json?iss.json=extended&iss.meta=off'
)


# Stack market данные. (Нет индекса Мосбиржи)
# STACK_MARKET_TOKEN = getenv('STACK_MARKET_TOKEN')
# SM_URL = (
#    f'http://api.marketstack.com/v1/eod?access_key = {STACK_MARKET_TOKEN}'
# )

TYPE_DATA_IMOEX = ['securities', 'marketdata']
NEEDFUL = [
    'SECID', 'SHORTNAME', 'PREVPRICE', 'PREVWAPRICE', 'PREVDATE',
    'STATUS', 'WAPTOPREVWAPRICE', 'UPDATETIME', 'LCURRENTPRICE', 'LAST',
    'PRICEMINUSPREVWAPRICE',
]

FILE_MAIN = 'data_json/api_data.json'
FILE_UP_PRICE = 'data_json/up_in_price.json'
FILE_DOWN_PRICE = 'data_json/down_in_price.json'


def start_message(name):
    hello_message = (
        f'👋Приветсвую, {name}!\n\n '
    )
    disclaimer_message = (
        '💰📈 Бот предоставляет прогнозы по акциям с анализом роста/падения.\n\n'
        'Перед работой обязательно ознакомтесь с дополнительной информации '
        '"/info"❗️\n\n'
    )
    return hello_message + disclaimer_message


def info_message():
    message = ('📊 Информация о боте финансовой аналитики\n\n'
               '💸 Наш бот использует данные с Мосбиржи, анализирует их с '
               'помощью алгоритмов '
               'технического анализа и предоставляет прогнозы по акциям '
               '(рост или падение), чтобы помочь вам увеличить свой капитал.'
               '\n\n📈 Будьте в курсе актуальных новостей и трендов для '
               'принятия взвешенных решений.\n\n'
               '🏆 Используйте нашего бота для получения знаний в финансовой '
               'аналитике и инвестирования.\n\n'
               '⚠️ Обратите внимание, что мы не несем ответственности за '
               'последствия ваших '
               'решений. Помните о возможных рисках, связанных с самой '
               'природой экономики.'
               '\n\n✍️ Автор (разработчик): @Vasilianin\n'
               '🤝 Если у вас есть какие-либо вопросы или предложения, '
               'пожалуйста, свяжитесь со мной.')
    return message
