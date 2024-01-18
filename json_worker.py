import requests
import json
import logging

from data import NEEDFUL, handler

logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class JSONSaveAndRead():
    """ Запись  и чтение полученного json файла."""
    def __init__(self, url, file) -> None:
        self.url = url
        self.file = file

    @classmethod
    def get_api_response(self):
        return requests.get(self.url).json()

    @classmethod
    def save_api_request(self, data):
        with open(self.file, 'w') as outfile:
            json.dump(data, outfile)

    @classmethod
    def read_api_request(self):
        with open(self.file) as json_file:
            return json.load(json_file)


class JSONSaveAndReadISS(JSONSaveAndRead):
    """ Запись  и чтение полученного json файла."""
    def __init__(self, url, file, type_data) -> None:
        super().__init__(url, file)
        self.type_data = type_data

    @classmethod
    def api_response_filter(self):
        result = []
        resp = self.test_indata(
            indata=self.get_api_response(),
            type_data=self.type_data
        )
        for element in resp[1][self.type_data]:
            new_dict = {}
            for key, value in element.items():
                if key in NEEDFUL:
                    new_dict[key] = value
            result.append(new_dict)
        return self.test_outdata(result)

    def test_indata(indata, type_data):
        try:  # Структура входных данных.
            if not isinstance(indata, list):
                raise TypeError('indata - not list')
            if not isinstance(indata[1], dict):
                raise TypeError('indata[1] - not dict')
            if type_data not in indata[1].keys():
                raise ValueError(
                    f'indata[1] - "{type_data}" not in indata[1]'
                )
            if not isinstance(indata[1][type_data], list):
                raise TypeError(f'indata[1]["{type_data}"] - not list')
            if not isinstance(indata[1][type_data][0], dict):
                raise TypeError(f'indata[1]["{type_data}"][0] - not dict')
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
