from os import getenv
import sys

from dotenv import load_dotenv
import logging

from json_worker import JSONSaveAndRead

handler = logging.StreamHandler(sys.stdout)
formater = logging.Formatter(
    '%(name)s, %(asctime)s, %(levelname)s - %(message)s.'
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
    'PRICEMINUSPREVWAPRICE', 'TIME'
]

FILE_MAIN = 'data_json/api_data.json'
FILE_UP_PRICE = 'data_json/up_in_price.json'
FILE_DOWN_PRICE = 'data_json/down_in_price.json'


def start_message(name):
    hello_message = (
        f'Приветсвую, {name}!\n\n '
    )
    disclaimer_message = (
        'Перед началом обязательно прочитай "/info"'
        'Если тебе понравился бот и ты хочешь, чтобы '
        'я улучшал его, то дай обратную связь: \n ---> @Vasilianin.\n\n'
    )
    return hello_message + disclaimer_message


def info_message():
    message = ''
    return message
