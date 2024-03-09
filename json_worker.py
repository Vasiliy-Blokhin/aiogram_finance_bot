""" Описание класса, для работы с БД."""
import requests
import json
import logging
from datetime import datetime
from pytz import timezone

from settings import (
    NEEDFUL, handler, STATUS_UP, STATUS_DOWN,
    STOP_TRADING, RUN_TRADING, FILE_MAIN, STATUS_MEDIUM,
    FILE_UP_PRICE, FILE_DOWN_PRICE)
from algorithm_module import interp_4_dote, interp_6_dote

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
    def api_response_filter(self):
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
    def union_api_response(self, data_sec, data_md):
        """ Добавляет доплнительные параметры и сводит всё в одну БД."""
        result = []
        logger.debug('до проверки сессии')
        for el_sec in data_sec:
            for el_md in data_md:
                # Сведение БД в одну.
                if el_sec['SECID'] == el_md['SECID']:
                    el_sec.update(el_md)
            # Добавление новых параметров.
            if el_sec['TRADINGSESSION'] is None:
                el_sec['TRADINGSESSION'] = STOP_TRADING
            elif el_sec['TRADINGSESSION'] == '1':
                el_sec['TRADINGSESSION'] = RUN_TRADING

            if el_sec['CURRENCYID'] == 'SUR':
                el_sec['CURRENCYID'] = 'рубль'

            format = '%H:%M:%S (%d.%m)'
            el_sec['DATAUPDATE'] = (
                datetime.now(timezone('Europe/Moscow'))
            ).strftime(format)

            result.append(el_sec)
        # Проверка и вывод выходных данных.
        logger.debug('после проверки сессии')
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

    @classmethod
    def score_counter_and_filter(self):
        data = self.read_api_request(file=FILE_MAIN)
        max_score = 21  # Максимальный балл (вручную)

        data_up = []
        data_down = []

        for share in data:
            try:
                current_score = 0

                current_score += interp_4_dote(
                    dote_prcnt=share['WAPTOPREVWAPRICEPRCNT'],
                    point_limits=[-4, 4],
                    prcnt_limits=[-4, 4],
                    prcnt_start_limit=0.2
                )

                if share['LCURRENTPRICE'] > share['LAST']:
                    current_score += 1
                elif share['LCURRENTPRICE'] < share['LAST']:
                    current_score -= 1

                current_score += interp_6_dote(
                    dote_prcnt=share['PRICEMINUSPREVWAPRICE']/share['WAPRICE'],
                    point_limits=[-6, 6],
                    prcnt_limits=[-4, -1.2, 1.2, 4],
                    prcnt_start_limit=0.2
                )

                capitalization_diff = (
                    share['TRENDISSUECAPITALIZATION']
                    / share['ISSUECAPITALIZATION']
                )
                current_score += interp_4_dote(
                    dote_prcnt=capitalization_diff,
                    point_limits=[-4, 4],
                    prcnt_limits=[-6, 6],
                    prcnt_start_limit=0.3
                )

                current_score += interp_4_dote(
                    dote_prcnt=share['LASTCNGTOLASTWAPRICE']/share['WAPRICE'],
                    point_limits=[-4, 4],
                    prcnt_limits=[-3, 3],
                    prcnt_start_limit=0.1
                )

                current_score += -interp_4_dote(
                    dote_prcnt=share['LASTCHANGEPRCNT'],
                    point_limits=[-2, 2],
                    prcnt_limits=[-1, 1],
                    prcnt_start_limit=0.05
                )

                share['FILTER_SCORE'] = 100 * current_score / max_score

                if share['FILTER_SCORE'] >= 70:
                    share['STATUS_FILTER'] = STATUS_UP
                    data_up.append(share)
                elif share['FILTER_SCORE'] <= -70:
                    share['STATUS_FILTER'] = STATUS_DOWN
                    data_down.append(share)
                else:
                    share['STATUS_FILTER'] = STATUS_MEDIUM

            except Exception:
                continue

        self.save_api_request(file=FILE_MAIN, data=data)
        self.save_api_request(file=FILE_UP_PRICE, data=data_up)
        self.save_api_request(file=FILE_DOWN_PRICE, data=data_down)


class JSONUpData(JSONSaveAndReadISS):
    pass


class JSONDownData(JSONSaveAndReadISS):
    pass
