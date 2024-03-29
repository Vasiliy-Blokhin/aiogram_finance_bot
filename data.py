from os import getenv
import sys

from dotenv import load_dotenv
import logging

# Описание хандлера для логгера.
handler = logging.StreamHandler(sys.stdout)
formater = logging.Formatter(
    '%(name)s, %(funcName)s, %(asctime)s, %(levelname)s - %(message)s.'
)
handler.setFormatter(formater)

load_dotenv()

TOKEN = getenv('BOT_TOKEN')

# URL для получения данных Мосбиржи.
IMOEX_URL = (
    'http://iss.moex.com/iss/engines/stock/markets/shares/'
    'securities.json?iss.json=extended&iss.meta=off'
)

# Stack market данные. (Нет информации индекса Мосбиржи)
# STACK_MARKET_TOKEN = getenv('STACK_MARKET_TOKEN')
# SM_URL = (
#    f'http://api.marketstack.com/v1/eod?access_key={STACK_MARKET_TOKEN}'
# )

# "Графы" и поля, необходимые для сбора данных.
TYPE_DATA_IMOEX = ['securities', 'marketdata']
NEEDFUL = [
    'SECID', 'SHORTNAME', 'PREVPRICE', 'PREVWAPRICE', 'PREVDATE',
    'STATUS', 'WAPTOPREVWAPRICE', 'UPDATETIME', 'LCURRENTPRICE', 'LAST',
    'PRICEMINUSPREVWAPRICE', 'DATAUPDATE', 'CURRENCYID', 'TRADINGSESSION',
    'STATUS_FILTER'
]

# Пути файлов для БД.
FILE_MAIN = 'data_json/api_data.json'
FILE_UP_PRICE = 'data_json/up_in_price.json'
FILE_DOWN_PRICE = 'data_json/down_in_price.json'

# Параметры для вывода сообщений.
PARAMS_ALL = {
    'SECID': 'Код',
    'SHORTNAME': 'Название',
    'UPDATETIME': 'Время последнего обновления',
    'LAST': 'Последняя цена (за акцию)',
    'DATAUPDATE': 'Время последнего обновления базы данных',
    'CURRENCYID': 'Валюта',
    'TRADINGSESSION': 'Текущая сессия',
    'STATUS_FILTER': 'Статус фильтрации'
}
