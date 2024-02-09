import asyncio
import logging
import sys
import env

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineQuery, CallbackQuery
from aiogram.utils.markdown import hbold
from aiogram import F

from bs_orm import Requests
import global_info.global_data as global_data
from processing import models
from processing import data_processing, db_processing
from global_info.keyboards import *


TOKEN = env.__token__

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if not db_processing.create_user(message.from_user.id):
        await message.answer(f"Вы уже занесены в систему")
    else:
        await message.answer(
            f"Доброго времени суток, {hbold(message.from_user.full_name)}!\n Далее для прохождения верификации вам необходимо будет ответить на нескорлько вопросов")
    await any_one_message(message, True)


@dp.message()
async def any_one_message(message: Message, from_start=False):
    status = db_processing.get_user_status(message.from_user.id)
    if status < 5:
        if not from_start:
            result, status_result = data_processing.check_answer(message.text,
                                                                 status,
                                                                 global_data.new_user_data['column_name'][status] if status < 3 else global_data.bank_data['column_name'][status-3])
            if not status_result:
                await message.answer(f'В ответе допущена ошибка: {result}. Попробем ешё раз?')
            else:
                if status < 2 or str(result) == '0':
                    db_processing.save_user_data(message.from_user.id,
                                                 global_data.new_user_data['column_name'][status], result)
                elif status == 2 and result == 1:
                    db_processing.save_user_data(message.from_user.id,
                                                 global_data.new_user_data['column_name'][status],
                                                 result, 3)
                    await message.answer(
                        f'Вы успешно зарегистрированны в системе')
                    await any_one_message(message, True)
                    return
                elif status > 2:
                    db_processing.create_bank(message.from_user.id)
                    db_processing.save_bank_data(message.from_user.id,
                                                 global_data.bank_data['column_name'][status-3], result)
                status = db_processing.get_user_status(message.from_user.id)
        if status < 3:
            await message.answer(
                f'Введите {global_data.new_user_data["user_view"][status]}')
        elif status < 5:
            await message.answer(
                f'Введите {global_data.bank_data["user_view"][status-3]}')
        else:
            await any_one_message(message)

    else:
        if message.text == "✅На что я уже подписался?)✅":
            if db_processing.get_magazine_station():
                if magazin := db_processing.get_magazin(message.from_user.id) \
                        == None:
                    magazin = "Не указан"
                if count_roses := db_processing.get_count_roses(message.from_user.id) \
                        == None:
                    count_roses = 'Не указан'
                await message.answer(
                    f'Вы обязаны:\n\t\tПодойти в магазин по адресу: {magazin}\n\t\tПрихватив с собой розы в количестве {count_roses} шт.')
            else:
                await message.answer(f'Пока что вы не выбирали магазинов :(')
        elif message.text == "💸Хочу задонатить":
            data = db_processing.get_bank_info()
            user_info = ''
            if len(data) == 0:
                await message.answer(
                    f"К сожадению в данный момент нет людей готовых заняться закупкой, попробуйте позже :(")
            for i in data:
                user_info += f'\nБанк: {i["name"]}\nРеквизиты: {i["data"]}\n'
            await message.answer(f"Вы можете осуществить перевод по реквизитам: {user_info}\nСПАСИБО за вашу помщь в этой непростой задумке🙃")
        elif message.text == "Хочу пойти в магазин и подарить розы🌹":
            await message.answer(f'Если вы хотите выбрать магазин в котором будете дарить розы, напишите мне "@{bot._me.username} город_роз"', reply_markup=main_keyboard())
        elif message.text == "💳Изменить реквизиты для перевода💳":
            db_processing.set_status(message.from_user.id, 3)
            await any_one_message(message, True)
        else:
            need_data = data_processing.search_item(
                message.text.replace(f'{bot._me.username} город_роз', ''))
            if need_data != None:
                additionally = ''
                if db_processing.get_purchase_consent(message.from_user.id):
                    additionally += f"(Мы переведём вам {need_data['count_roses']*300})"
                await message.answer(f"Вы уверены что смоэете прийти в магазин по адрессу:\n{need_data['addres']}\nЗаранее купив {need_data['count_roses']}\n И Быть у магазина ровно в 10:00 07.03.2024?"+additionally, reply_markup=magazin_keyboard())
            else:
                await message.answer("Данные обновлены :)", reply_markup=main_keyboard())


@dp.inline_query()
async def inline_echo(inline_query: InlineQuery) -> None:
    items = []
    if db_processing.get_user_status(inline_query.from_user.id) >= 5 and \
                'город_роз' in inline_query.query and \
                inline_query.chat_type == 'sender':
        items = data_processing.get_list_item(
            [], inline_query.query.replace('город_роз', '').strip())

    await bot.answer_inline_query(
        inline_query_id=inline_query.id,
        results=items,
        cache_time=1,
        is_personal=True
    )


@dp.callback_query(MyCallback.filter(F.bar != ''))
async def yes_btn(query: CallbackQuery, callback_data: MyCallback):
    db_processing.set_magazin_station(query.from_user.id, callback_data.bar)
    await query.message.answer("Хорошо, я запомнил твой ответ", \
                               reply_markup=main_keyboard())


async def main() -> None:

    Requests.db_settings.models = models
    # Requests.migrate()
    Requests.create_tables()

    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
