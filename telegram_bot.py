""" Основной исполняемый файл (запуск бота). """
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from settings import PARAMS_ALL, TOKEN, handler
from message_builder import (certain_shares, counter_message, error_message,
                             info_message, instruction_message, risk_message,
                             shares_mess, start_message, statistic_message)
from data_processor import ALL_JC, DOWN_JC, UP_JC

logger = logging.getLogger(name=__name__)  # Запуск логга проекта.
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

dp = Dispatcher()

# Словарь для фильтрации команд (сообщений) вводимых пользователем.
SPLIT_JS = {
    '/up': UP_JC,
    '/down': DOWN_JC,
    '/all': ALL_JC,
}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Стартовый набор команд (сообщений).
    """
    kb = [
        [
            types.KeyboardButton(text='/start'),  # Сообщение старт.
            types.KeyboardButton(text='/info'),  # Сообщение информации.
            # Сообщение информации о рисках.
            types.KeyboardButton(text='/risk'),
            # Инструкции для работы с ботом.
            types.KeyboardButton(text='/instr'),
            types.KeyboardButton(text='/count'),  # Вывод информации о БД.
            # Вывод информации о статистике.
            types.KeyboardButton(text='/statistic'),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder=('Не забудьте ознакомиться с информацией '
                                 '"/instr".')
    )
    await message.answer(  # Сообщение старт.
        start_message(message.from_user.first_name),
        reply_markup=keyboard
    )


@dp.message(F.text.lower() == '/info')
async def info_button(message: types.Message):
    """ Вывод сообщения - общей информации."""
    await message.reply(info_message())


@dp.message(F.text == '/risk')
async def risk_button(message: types.Message):
    """ Вывод сообщения информации о возможных рисках."""
    await message.reply(risk_message())


@dp.message(F.text == '/instr')
async def instruction_button(message: types.Message):
    """ Вывод сообщения-инструкции по работе с ботом."""
    await message.reply(instruction_message())


@dp.message(F.text == '/count')
async def counter_button(message: types.Message):
    """ Вывод информации о БД."""
    await message.reply(counter_message())


@dp.message(F.text.lower() == '/statistic')
async def info_button(message: types.Message):
    """ Вывод сообщения - общей информации."""
    await message.reply(statistic_message())


@dp.message()
async def shares_button(message: types.Message):
    """ Обработчик сообщений."""
    try:
        split_msg = message.text.split('_')

        # Вывод сообщения ошибки, если ввод не соответсвует инструкции.
        if len(split_msg) >= 4 or len(split_msg) < 2:
            await message.reply(text=error_message())
            return False

        if split_msg[0] in SPLIT_JS:
            limit = int(split_msg[1])
            offset = 0
        # Вывод сообщения ошибки, если ввод не соответсвует инструкции.
            if limit > 10:
                await message.reply(text=error_message())
                return False
            if len(split_msg) >= 3:
                offset = int(split_msg[2])

            # Выбор БД, в зависимости от запроса.
            all_data = SPLIT_JS[split_msg[0]].read_api_request()

            for data in all_data:
                # Выполнение функции пропуска определенного числа элементов,
                # если пользователь задал этот параметр.
                if offset:
                    offset -= 1
                    continue

                # Формирование вывод-сообщения (шаблона) с показателями акции.
                current_message = ''
                for key, value in data.items():
                    if key in PARAMS_ALL.keys():
                        current_message += (
                            shares_mess(key, value)
                        )
                current_message += '\n'
                # Отправка сформированного сообщения.
                await message.reply(current_message)

                # Выполнения функции вывода определенного количества акций.
                limit -= 1
                if limit == 0:
                    break
        # Вывод отдельной акции по коду (по инструкции).
        elif split_msg[0] == '/shares':
            if not isinstance(split_msg[1], str):
                await message.reply(error_message())
            text = split_msg[1].upper()
            await message.reply(text=certain_shares(text))
        # Вывод сообщения ошибки, если ввод не соответсвует инструкции.
        else:
            await message.reply(text=error_message())
            return False
    except Exception as error:
        logger.error(f"bot error ---> {error}")
        await message.reply(error_message())


async def main() -> None:
    """ Выполнение основной части работы бота."""
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
