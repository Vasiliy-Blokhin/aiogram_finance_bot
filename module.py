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


class JSONSaveAndRead():
    """ Запись  и чтение полученного json файла."""
    def __init__(self, url) -> None:
        self.url = url

    @classmethod
    def get_api_response(self):
        result = []
        resp = self.test_indata(requests.get(self.url).json())
        for element in resp[1]['securities']:
            new_dict = {}
            for key, value in element.items():
                if key in NEEDFUL:
                    new_dict[key] = value
            result.append(new_dict)
        return self.test_outdata(result)

    def test_indata(indata):
        try:  # Структура входных данных.
            if not isinstance(indata, list):
                raise TypeError('indata - not list')
            if not isinstance(indata[1], dict):
                raise TypeError('indata[1] - not dict')
            if 'securities' not in indata[1].keys():
                raise ValueError('indata[1] - "securities" not in indata[1]')
            if not isinstance(indata[1]['securities'], list):
                raise TypeError('indata[1]["securities"] - not list')
            if not isinstance(indata[1]['securities'][0], dict):
                raise TypeError('indata[1]["securities"][0] - not dict')
            if not set(NEEDFUL).issubset(indata[1]['securities'][0]):
                raise ValueError('needful not in indata[1]["securities"][0]')
            return indata
        except Exception as error:
            logger.error(f'Error ---> {error}')
            return False

    def test_outdata(outdata):
        try:  # Структура выходных данных.
            if not isinstance(outdata, list):
                raise TypeError('outdata - not list')
            for element in outdata:
                if not isinstance(element, dict):
                    raise TypeError('outdata[element] - not dict')
                if not set(element.keys()).issubset(NEEDFUL):
                    raise ValueError('outdata[element] - not in needful')
            return outdata
        except Exception as error:
            logger.error(f'Error ---> {error}')
            return False

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
