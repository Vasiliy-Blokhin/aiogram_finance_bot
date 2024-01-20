import logging
from time import sleep

from data import (
    IMOEX_URL, FILE_MAIN, handler, TYPE_DATA_IMOEX,
    FILE_UP_PRICE, FILE_DOWN_PRICE
)
from json_worker import JSONSaveAndReadISS, JSONDownData, JSONUpData


logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


ALL_JC = JSONSaveAndReadISS
ALL_JC.url = IMOEX_URL
ALL_JC.file = FILE_MAIN

UP_JC = JSONUpData
UP_JC.file = FILE_UP_PRICE

DOWN_JC = JSONDownData
DOWN_JC.file = FILE_DOWN_PRICE


def get_data(api_json_class):
    data_list = []
    for type_data in TYPE_DATA_IMOEX:
        api_json_class.type_data = type_data
        data = api_json_class.api_response_filter()
        data_list.append(data)
    return api_json_class.union_api_response(*data_list)


def filter_data(jcs, data):
    for jc in jcs:
        jc.save_api_request(
            jc.data_filter_daily(data=data)
        )


if __name__ == '__main__':
    # Работа мосбиржи.
    while True:
        try:
            ALL_JC.save_api_request(get_data(ALL_JC))

            filter_data(
                [UP_JC, DOWN_JC],
                ALL_JC.read_api_request()
            )
        except Exception as error:
            logger.error(f'Module error ---> {error}')
        finally:
            sleep(600)
