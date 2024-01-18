import logging

from data import IMOEX_URL, FILE_MAIN, SM_URL, handler
from json_worker import JSONSaveAndReadISS


logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


if __name__ == '__main__':
    # Работа мосбиржы.
    JSONSaveAndReadISS.url = IMOEX_URL
    JSONSaveAndReadISS.file = FILE_MAIN
    data = JSONSaveAndReadISS.api_response_filter()
    JSONSaveAndReadISS.save_api_request(data=data)
    logger.info(f'result (ISS) ---> {JSONSaveAndReadISS.read_api_request()}')
