from os import getenv

from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

# IMOEX данные
IMOEX_URL = (
    'http://iss.moex.com/iss/engines/stock/markets/shares/'
    'securities.json?iss.json=extended&iss.meta=off'
    )

NEEDFUL = [
    'SECID', 'SHORTNAME', 'PREVPRICE', 'PREVWAPRICE', 'PREVDATE', 'SETTLEDATE'
]


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
