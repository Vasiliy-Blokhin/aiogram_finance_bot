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
            api_json_class = JSONSaveAndReadISS
            api_json_class.url = IMOEX_URL
            api_json_class.file = FILE_MAIN
            api_json_class.save_api_request(get_data(api_json_class))

            if api_json_class.read_api_request()[0]['LAST'] is None:
                continue

            up_json_class = JSONUpData
            up_json_class.file = FILE_UP_PRICE
            down_json_class = JSONDownData
            down_json_class.file = FILE_DOWN_PRICE
            filter_data(
                [up_json_class, down_json_class],
                api_json_class.read_api_request()
            )
        except Exception as error:
            logger.error(f'Module error ---> {error}')
        finally:
            sleep(600)
