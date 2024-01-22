""" Работа с формированием базы данных."""
import logging
from time import sleep

from data import (
    IMOEX_URL, FILE_MAIN, handler, TYPE_DATA_IMOEX,
    FILE_UP_PRICE, FILE_DOWN_PRICE
)
from json_worker import JSONSaveAndReadISS, JSONDownData, JSONUpData


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
                data['STATUS_FILTER'] = 'вероятность роста'
                data_st['STATUS_FILTER'] = 'вероятность роста'
        UP_JC.save_api_request(up_data)

        down_data = DOWN_JC.read_api_request()
        for data_st in down_data:
            if data['SECID'] == data_st['SECID']:
                data['STATUS_FILTER'] = 'вероятность падения'
                data_st['STATUS_FILTER'] = 'вероятность падения'
        DOWN_JC.save_api_request(down_data)

    ALL_JC.save_api_request(all_data)


def main():
    """ Общая логика работы."""
    while True:
        try:
            get_and_save_data(ALL_JC)
            filter_data(
                [UP_JC, DOWN_JC],
                ALL_JC.read_api_request()
            )
            add_more_information()
        except Exception as error:
            logger.error(f'Module error ---> {error}')
        finally:
            sleep(60)


if __name__ == '__main__':
    main()
