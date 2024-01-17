import sys

import requests
import json
import logging

from data import IMOEX_URL, NEEDFUL


logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
formater = logging.Formatter(
    '%(name)s, %(asctime)s, %(levelname)s - %(message)s.'
)
handler.setFormatter(formater)

logger.addHandler(handler)


# request 1 for 10000 sec
class JSONSaveAndRead():
    """ Запись  и чтение полученного json файла."""
    def __init__(self, url) -> None:
        self.url = url
    @classmethod
    def get_api_response(self):
        result = []
        resp = list(requests.get(self.url).json())
        #Структура ответа.
        # logger.info(f'resp -> {type(resp)}') # list
        # logger.info(f'resp[1] -> {type(resp[1])} - {resp[1].keys()}') # dict
        # logger.info(f'resp[1]["securities"] -> {type(resp[1]["securities"])}') # list
        # logger.info(f'resp[1]["securities"][0] -> {type(resp[1]["securities"][0])}') # dict
        for element in resp[1]["securities"]:
            new_dict = {}
            for key, value in element.items():
                if key in NEEDFUL:
                    new_dict[key] = value
            result.append(new_dict)
        return result



    @classmethod
    def save_api_request(self):
        data = self.get_api_response()
        with open('api_data.json', 'w') as outfile:
            json.dump(data, outfile)

    @classmethod
    def read_api_request(self):
        with open('api_data.json') as json_file:
            return json.load(json_file)


if __name__ == '__main__':
    JSONSaveAndRead.url = IMOEX_URL
    JSONSaveAndRead.get_api_response()
    JSONSaveAndRead.save_api_request()
    logger.info(f'result ---> {JSONSaveAndRead.read_api_request()}')
