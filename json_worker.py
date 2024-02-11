""" Описание класса, для работы с БД."""
import requests
import json
import logging
from datetime import datetime
from pytz import timezone

from data import NEEDFUL, handler, STATUS_UP, STATUS_DOWN

# Запуск логгера.
logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class JSONSaveAndRead():
    """ Родительский класс для базовых действий."""
    def __init__(self, url: str | None, file: str) -> None:
        self.url: str | None = url
        self.file: str = file

    @classmethod
    def get_api_response(self):
        """ Получение информации с запроса на сервер."""
        return requests.get(self.url).json()

    @classmethod
    def save_api_request(self, data, file=None):
        """ Сохранение информации в файле."""
        if file is None:
            file = self.file
        with open(file, 'w') as outfile:
            json.dump(data, outfile)

    @classmethod
    def read_api_request(self, file=None):
        """ Чтение информации с файла."""
        if file is None:
            file = self.file
        with open(file) as json_file:
            return json.load(json_file)

    class Meta:
        abstract = True


class JSONSaveAndReadISS(JSONSaveAndRead):
    """ Класс для работы с API imoex (iss)."""
    def __init__(self, url, file, type_data: str) -> None:
        super().__init__(url, file)
        self.type_data: str = type_data

    @classmethod
    def api_response_filter(self) -> list[dict] | bool:
        """ Фильтрация данных, полученных с запроса."""
        result = []
        # Получение и проверка данных.
        resp = self.validate_indata(
            indata=self.get_api_response(),
            type_data=self.type_data
        )
        # Фильтрация полученных данных (из разных "графов").
        for element in resp[1][self.type_data]:
            # Оставляет только акции.
            if (self.type_data == 'securities'
                and element.get('INSTRID') != 'EQIN'):
                continue
            new_dict = {}
            # Добавление только необходимых параметров из списка.
            for key, value in element.items():
                if key in NEEDFUL:
                    new_dict[key] = value
            result.append(new_dict)
        # Проверка и вывод результатов.
        return self.validate_outdata(result)

    @classmethod
    def union_api_response(self, data_sec: list[dict], data_md):
        """ Добавляет доплнительные параметры и сводит всё в одну БД."""
        result = []
        for el_sec in data_sec:
            for el_md in data_md:
                # Сведение БД в одну.
                if el_sec['SECID'] == el_md['SECID']:
                    el_sec.update(el_md)
            # Добавление новых параметров.
            if el_sec['TRADINGSESSION'] is None:
                el_sec['TRADINGSESSION'] = 'торги приостановлены'
            elif el_sec['TRADINGSESSION'] == '1':
                el_sec['TRADINGSESSION'] = 'торги идут'

            if el_sec['CURRENCYID'] == 'SUR':
                el_sec['CURRENCYID'] = 'рубль'

            format = '%H:%M:%S (%d.%m)'
            el_sec['DATAUPDATE'] = (
                datetime.now(timezone('Europe/Moscow'))
            ).strftime(format)

            result.append(el_sec)
        # Проверка и вывод выходных данных.
        return self.validate_outdata(result)

    def validate_indata(indata, type_data: str) -> list[dict] | bool:
        """ Валидация входных данных (видна структура вх. данных)."""
        try:
            if indata is None:
                raise ValueError('indata - empty.')
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
            logger.error(f'Indata error ---> {error}')
            return False

    def validate_outdata(outdata) -> list[dict] | bool:
        """ Валидация выходных данных (видна структура вых. данных)."""
        try:
            if outdata is None:
                raise ValueError('outdata - empty.')
            if not isinstance(outdata, list):
                raise TypeError('outdata - not list')
            for element in outdata:
                if not isinstance(element, dict):
                    raise TypeError('outdata[element] - not dict')
                if not set(element.keys()).issubset(NEEDFUL):
                    raise ValueError('outdata[element] - not in needful')
            return outdata
        except Exception as error:
            logger.error(f'Outdata error ---> {error}')
            return False


class JSONUpData(JSONSaveAndReadISS):
    """ Класс для фильтрации данных (повыш. роста)."""
    def data_filter_last(data):
        """ Показатели на день."""
        result = []
        for el in data:
            el['STATUS_FILTER'] = STATUS_UP
            if el['STATUS'] != 'A':
                continue
            if el['PREVPRICE'] is None or el['PREVWAPRICE'] is None:
                continue
            if el['PREVPRICE'] < el['PREVWAPRICE']:
                continue
            result.append(el)
        return result

    @classmethod
    def data_filter_daily(self, data):
        """ Показатели в зависимости от текущих данных."""
        result = []
        params = [
            'WAPTOPREVWAPRICE', 'PRICEMINUSPREVWAPRICE', 'LCURRENTPRICE',
            'PREVWAPRICE', 'LAST'
        ]
        for el in self.data_filter_last(data):
            param_log = True
            for param in params:
                if el[param] is None:
                    param_log = False
            if not param_log:
                continue
            if el['WAPTOPREVWAPRICE'] < 0:
                continue
            if el['PRICEMINUSPREVWAPRICE'] < 0:
                continue
            if el['LCURRENTPRICE'] < el['PREVWAPRICE']:
                continue
            if el['LCURRENTPRICE'] < el['LAST']:
                continue
            if el['LAST'] < el['PREVWAPRICE']:
                continue
            result.append(el)
        return result


class JSONDownData(JSONSaveAndReadISS):
    """ Класс для фильтрации данных (пад. цены)."""
    def data_filter_last(data):
        """ Показатели на день."""
        result = []
        for el in data:
            el['STATUS_FILTER'] = STATUS_DOWN
            if el['STATUS'] != 'A':
                continue
            if el['PREVPRICE'] is None or el['PREVWAPRICE'] is None:
                continue
            if el['PREVPRICE'] > el['PREVWAPRICE']:
                continue
            result.append(el)
        return result

    @classmethod
    def data_filter_daily(self, data):
        """ Показатели в зависимости от текущих данных."""
        result = []
        params = [
            'WAPTOPREVWAPRICE', 'PRICEMINUSPREVWAPRICE', 'LCURRENTPRICE',
            'PREVWAPRICE', 'LAST'
        ]
        for el in self.data_filter_last(data):
            param_log = True
            for param in params:
                if el[param] is None:
                    param_log = False
            if not param_log:
                continue
            if el['WAPTOPREVWAPRICE'] > 0:
                continue
            if el['PRICEMINUSPREVWAPRICE'] > 0:
                continue
            if el['LCURRENTPRICE'] > el['PREVWAPRICE']:
                continue
            if el['LCURRENTPRICE'] > el['LAST']:
                continue
            if el['LAST'] > el['PREVWAPRICE']:
                continue
            result.append(el)
        return result
