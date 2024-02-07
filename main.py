import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

import sql_execute
import global_data

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "2036817778:AAFzwMIhQta1LpKnr4MCNz2hlWKWMLhbn1Y"

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if (error := sql_execute.create_user(message.from_user.id)) != None:
        await message.answer(f'{error}. Пожалуйста, следуйте последней инструкции отправленной ранее')
    else:
        await message.answer(f"Добрый день, {hbold(message.from_user.full_name)}!\nПожалуйста, укажите ваше ФИО")

@dp.message()
async def any_one_message(message: Message):
    user_id = message.from_user.id
    status = sql_execute.get_status(user_id)
    if status <= max(global_data.first_data):
        status = sql_execute.update_status(user_id, input_value = message.text, status=status)
        if status <= max(global_data.first_data):
            await message.answer(f'Введите {global_data.first_data[status][0]}')
        else:
            await message.answer('Основные данные заполнены')
            # Вывод меню





async def main() -> None:
    sql_execute.create_table()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)



    asyncio.run(main())