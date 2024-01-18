from os import getenv
import sys

from dotenv import load_dotenv
import logging


handler = logging.StreamHandler(sys.stdout)
formater = logging.Formatter(
    '%(name)s, %(asctime)s, %(levelname)s - %(message)s.'
)
handler.setFormatter(formater)

load_dotenv()

TOKEN = getenv('BOT_TOKEN')
STACK_MARKET_TOKEN = getenv('STACK_MARKET_TOKEN')
# IMOEX данные
IMOEX_URL = (
    'http://iss.moex.com/iss/engines/stock/markets/shares/'
    'securities.json?iss.json=extended&iss.meta=off'
    )

# Stack market данные.
SM_URL = (
    f'http://api.marketstack.com/v1/eod?access_key = {STACK_MARKET_TOKEN}'
)
NEEDFUL = [
    'SECID', 'SHORTNAME', 'PREVPRICE', 'PREVWAPRICE', 'PREVDATE', 'SETTLEDATE'
]

FILE_MAIN = 'data_json/api_data.json'
FILE_UP_PRICE = 'data_json/up_in_price.json'
FILE_DOWN_PRICE = 'data_json/down_in_price.json'


def start_message(name):
    hello_message = (
        f'Приветсвую, {name}!\n\n Если тебе понравился бот и ты хочешь, чтобы '
        'я улучшал его, то дай обратную связь: \n ---> @Vasilianin.\n\n'
    )
    disclaimer_message = (
        'Дисклеймер:\n Результат, который выдает бот может '
        'быть ошибочным, так как данные берутся со сторонних сервисов '
        '(Мосбиржа).\n Акции'
        ' подбираются согласно расчетов различных методик, взятых из интернета и на'
        ' основе их выдаются рекомендации.\n Дальнейшие действия на ваш риск. '
        '\n\nНа данный момент бот находится в разработке, так что возможны '
        'отключения, сбои, неверная информация.'
    )
    return hello_message + disclaimer_message
