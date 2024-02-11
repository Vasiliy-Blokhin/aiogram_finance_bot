from datetime import datetime
import logging
from json_worker import JSONSaveAndRead
from data import STATISTIC_NEED, STATUS_UP, STATUS_DOWN, handler, FILE_DAILY_STATISTIC


# Подключение логгера.
logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


class StatisticModule(JSONSaveAndRead):
    """Сбор статистики о прогнозе."""
    def __init__(self, url: str | None, file: str, json_class, json_all_data) -> None:
        super().__init__(url, file)
        self.json_class = None
        self.json_all_data = json_all_data

    @classmethod
    def data_preparation(self):
        logger.info('start -> data_preparation')
        result = []
        for jsc in self.json_class:
            for el in jsc.read_api_request():
                count_dict = {}
                #if not self.is_trading_permission(self, el):
                #    return False

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
        count_positive = 0
        count_all = 0

        if not current_data:
            return False

        for el in self.json_all_data:
            for el_cd in current_data:

                if el['SECID'] == el_cd['SECID']:
                    el_cd['CUR_PRICE'] = el['LAST']
                    if el_cd['STATUS_FILTER'] == STATUS_UP:
                        if el_cd['CUR_PRICE'] > el_cd['LAST']:
                            count_positive += 1
                    if el_cd['STATUS_FILTER'] == STATUS_DOWN:
                        if el_cd['CUR_PRICE'] < el_cd['LAST']:
                            count_positive += 1
                    count_all += 1

        return f"{100 * count_positive/count_all} %"

    @classmethod
    def counting_statistics(self):
        logger.info('counting statistic.')
        data = self.read_api_request(file=FILE_DAILY_STATISTIC)

        daily_dict = {}
        daily_dict[datetime.now().strftime('%d.%m')] = self.get_current_price()

        all_daily = []
        all_daily.append(daily_dict)

        data.append({'DAILY': all_daily})
        logger.debug(f"data -> {data}")

        self.save_api_request(data=data, file=FILE_DAILY_STATISTIC)
