""" Работа с формированием базы данных."""
import logging
from time import sleep

from settings import (
    IMOEX_URL, FILE_MAIN, handler, TYPE_DATA_IMOEX,
    FILE_UP_PRICE, FILE_DOWN_PRICE, FILE_STATISTIC,
    TIME_UPDATE, SET_ITERATION, STOP_TRADING, STATUS_UP, STATUS_DOWN
)
from json_worker import JSONSaveAndReadISS, JSONDownData, JSONUpData
from statistic import StatisticModule

# Подключение логгера.
logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


# Подключение классов работы с БД.
ALL_JC = JSONSaveAndReadISS
ALL_JC.url = IMOEX_URL
ALL_JC.file = FILE_MAIN

UP_JC = JSONUpData
UP_JC.file = FILE_UP_PRICE

DOWN_JC = JSONDownData
DOWN_JC.file = FILE_DOWN_PRICE

STATISTIC_JS = StatisticModule
STATISTIC_JS.json_classes = [UP_JC, DOWN_JC]
STATISTIC_JS.json_all_data = ALL_JC.read_api_request()
STATISTIC_JS.url = None
STATISTIC_JS.file = FILE_STATISTIC


def get_and_save_data(api_json_class):
    """ Получение и формированией всей базы данных."""
    data_list = []
    for type_data in TYPE_DATA_IMOEX:
        # Определение "графы" для сбора данных.
        api_json_class.type_data = type_data
        # Отправка запроса, получение, первоначальная фильтрация.
        data = api_json_class.api_response_filter()
        data_list.append(data)
    # Сведение БД и сохранение.
    api_json_class.save_api_request(
        api_json_class.union_api_response(*data_list)
    )


def filter_data(jcs, data):
    """ Фильтрация и сохранение по БД (+ и - цены)."""
    for jc in jcs:
        jc.save_api_request(
            jc.data_filter_daily(data=data)
        )


def add_more_information():
    """ Добавление информации отработанной алгоритмом."""
    all_data = ALL_JC.read_api_request()
    for data in all_data:
        # Ввод результатов фильтрации.
        data['STATUS_FILTER'] = 'среднее значение'

        up_data = UP_JC.read_api_request()
        for data_st in up_data:
            if data['SECID'] == data_st['SECID']:
                data['STATUS_FILTER'] = STATUS_UP
                data_st['STATUS_FILTER'] = STATUS_UP
        UP_JC.save_api_request(up_data)

        down_data = DOWN_JC.read_api_request()
        for data_st in down_data:
            if data['SECID'] == data_st['SECID']:
                data['STATUS_FILTER'] = STATUS_DOWN
                data_st['STATUS_FILTER'] = STATUS_DOWN
        DOWN_JC.save_api_request(down_data)

    ALL_JC.save_api_request(all_data)


def main():
    """ Общая логика работы."""
    stat_counter = 0
    flag_preparation = True

    while True:
        try:
            logger.debug(f"Текущая итерация -> {stat_counter}")

            get_and_save_data(ALL_JC)

            if ALL_JC.read_api_request()[0]['TRADINGSESSION'] == STOP_TRADING:
                logger.info('Торги приостановлены, работа не ведется')
                continue

            filter_data(
                [UP_JC, DOWN_JC],
                ALL_JC.read_api_request()
            )
            add_more_information()
            logger.info('Данные успешно получены и отсортированы')

            if flag_preparation:
                logger.info('Обработка данных для статистики')
                STATISTIC_JS.data_preparation()
                flag_preparation = False

            if SET_ITERATION <= stat_counter:
                logger.info('Подсчет и вывод статистики')
                STATISTIC_JS.counting_statistics()
                flag_preparation = True
                stat_counter = 0

            stat_counter += 1

        except Exception as error:
            logger.error(f'Ошибка в модуле ---> {error}')
        finally:
            logger.info('Ожидание')
            sleep(TIME_UPDATE)


if __name__ == '__main__':
    main()
