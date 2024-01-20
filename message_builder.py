from module import ALL_JC, UP_JC
from data import PARAMS_ALL

import logging
from data import handler
logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


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


def risk_message():
    message = (
        ''
    )
    return message


def work_message():
    message = (
        ''
    )
    return message


def shares_mess(key, value, message):
    message += f"{PARAMS_ALL[key]} -> {value}\n"
    return message


def certain_shares(code):
    all_data = ALL_JC.read_api_request()
    for data in all_data:
        if data['SECID'] == code:
            share = data
            break
    message = (
        f"code -> {share['SECID']}\nname -> {share['SHORTNAME']}"
    )
    return message
