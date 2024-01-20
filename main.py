import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from data import TOKEN, handler, PARAMS_ALL
from message_builder import info_message, start_message, certain_shares, shares_mess, risk_message, instruction_message, counter_message, error_message
from module import UP_JC, ALL_JC, DOWN_JC

logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

dp = Dispatcher()


SPLIT_JS = {
    '/up_shares': UP_JC,
    '/down_shares': DOWN_JC,
    '/all_shares': ALL_JC,
}


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    kb = [
        [
            types.KeyboardButton(text='/start'),
            types.KeyboardButton(text='/info'),
            types.KeyboardButton(text='/risk'),
            types.KeyboardButton(text='/instr'),
            types.KeyboardButton(text='/counter'),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Не забудьте ознакомиться с информацией.'
    )
    await message.answer(start_message(message.from_user.first_name), reply_markup=keyboard)


@dp.message(F.text.lower() == '/info')
async def info_button(message: types.Message):
    await message.reply(info_message())


@dp.message(F.text == '/risk')
async def risk_button(message: types.Message):
    await message.reply(risk_message())


@dp.message(F.text == '/instr')
async def instruction_button(message: types.Message):
    await message.reply(instruction_message())


@dp.message(F.text == '/counter')
async def counter_button(message: types.Message):
    await message.reply(counter_message())


@dp.message()
async def shares_button(message: types.Message):
    split_msg = message.text.split()

    if split_msg[0] in SPLIT_JS:
        limit = int(split_msg[1])
        offset = None
        if limit > 10 or len(split_msg) >= 3:
            await message.reply(text=error_message())
            return False
        if len(split_msg) >= 3:
            offset = int(split_msg[2])

        all_data = SPLIT_JS[split_msg[0]].read_api_request()
        for data in all_data:
            data['STATUS_FILTER'] = 'среднее значение'
            for data_st in UP_JC.read_api_request():
                if data['SECID'] == data_st['SECID']:
                    data['STATUS_FILTER'] = 'вероятность роста'
            for data_st in DOWN_JC.read_api_request():
                if data['SECID'] == data_st['SECID']:
                    data['STATUS_FILTER'] = 'вероятность падения'
            if offset:
                offset -= 1
                continue
            current_message = ''
            for key, value in data.items():
                if key in PARAMS_ALL.keys():
                    current_message += (
                        shares_mess(key, value)
                    )
            current_message += '\n'
            await message.reply(current_message)
            limit -= 1
            if limit == 0:
                break
    elif split_msg[0] == '/shares':
        text = split_msg[1].upper()
        await message.reply(text=certain_shares(text))


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
