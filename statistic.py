from datetime import datetime
import logging
from json_worker import JSONSaveAndRead
from settings import STATISTIC_NEED, STATUS_UP, STATUS_DOWN, handler, FILE_DAILY_STATISTIC, COMISSION_COEFF, FILE_UP_ANOMALY


# Подключение логгера.
logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class StatisticModule(JSONSaveAndRead):
    """Сбор статистики о прогнозе."""
    def __init__(self, url: str | None, file: str, json_classes, json_all_data) -> None:
        super().__init__(url, file)
        self.json_classes = None
        self.json_all_data = json_all_data

    @classmethod
    def data_preparation(self):
        result = []
        for jsc in self.json_classes:
            for el in jsc.read_api_request():
                count_dict = {}

                for key, value in el.items():
                    if key in STATISTIC_NEED:
                        count_dict[key] = value
                result.append(count_dict)

        return self.save_api_request(result)

    def is_trading_permission(self, data):
        if data['TRADINGSESSION'] == 'торги приостановлены':
            return False
        return True

    @classmethod
    def get_current_price(self):
        current_data = self.read_api_request()
        count_positive_equals = 0
        count_positive_non_equals = 0
        count_all = 0
        count_price_before = 0
        count_price_after = 0

        for el in self.json_all_data:
            for el_cd in current_data:

                if el['SECID'] == el_cd['SECID']:
                    if el['LAST'] is None:
                        continue

                    el_cd['CUR_PRICE'] = el['LAST']

                    if el_cd['STATUS_FILTER'] == STATUS_UP:
                        if el_cd['CUR_PRICE'] >= el_cd['LAST']:
                            count_positive_equals += 1
                        else:
                            anomaly_data = self.read_api_request(
                                FILE_UP_ANOMALY
                            )
                            if anomaly_data is None:
                                anomaly_data = []
                            anomaly_data.append(el)
                            self.save_api_request(
                                file=FILE_UP_ANOMALY,
                                data=anomaly_data
                            )
                        if el_cd['CUR_PRICE'] > el_cd['LAST']:
                            count_positive_non_equals += 1

                        count_price_before += el_cd['CUR_PRICE']
                        count_price_after += el_cd['LAST']

                    if el_cd['STATUS_FILTER'] == STATUS_DOWN:
                        if el_cd['CUR_PRICE'] <= el_cd['LAST']:
                            count_positive_equals += 1
                        if el_cd['CUR_PRICE'] < el_cd['LAST']:
                            count_positive_non_equals += 1

                    count_all += 1

        count_positive = (count_positive_equals + count_positive_non_equals) / 2
        statistic_prcnt = float(100 * count_positive/count_all)

        comission = count_price_after * COMISSION_COEFF
        potential_profitability = count_price_before - count_price_after - comission
        if potential_profitability > 0:
            potential_profitability *= 0.87
        return [statistic_prcnt, count_price_after, potential_profitability]

    @classmethod
    def counting_statistics(self):
        data = self.read_api_request(file=FILE_DAILY_STATISTIC)
        if data is None:
            data = []

        data.append(self.get_current_price())

        self.save_api_request(data=data, file=FILE_DAILY_STATISTIC)
