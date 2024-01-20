import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from data import TOKEN, handler
from message_builder import info_message, start_message


logger = logging.getLogger(name=__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    kb = [
        [
            types.KeyboardButton(text='/info')
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Ознакомтесь.'
    )
    await message.answer(start_message(message.from_user.first_name), reply_markup=keyboard)


@dp.message(F.text.lower() == '/info')
async def info_button(message: types.Message):
    await message.reply(info_message())


@dp.message()
async def set_object(message: types.Message):
    try:
        await message.answer(text=message.text)
    except Exception as error:
        logger.error(f'Error ---> {error}')


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
