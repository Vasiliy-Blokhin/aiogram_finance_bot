import logging

from data import IMOEX_URL, FILE_MAIN, handler, TYPE_DATA_IMOEX
from json_worker import JSONSaveAndReadISS


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


if __name__ == '__main__':
    # Работа мосбиржы.
    api_json_class = JSONSaveAndReadISS
    api_json_class.url = IMOEX_URL
    api_json_class.file = FILE_MAIN
    api_json_class.save_api_request(get_data(api_json_class))
    print(api_json_class.read_api_request())
