from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class MyCallback(CallbackData, prefix="my"):
    bar: int

def magazin_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Да",
        callback_data=MyCallback(bar=1)
    )
    builder.button(
        text="Нет",
        callback_data=MyCallback(bar=0)
    )
    return builder.as_markup(resize_keyboard=True)

def main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(
        text="Хочу пойти в магазин и подарить розы🌹",
    )
    builder.button(
        text="💸Хочу задонатить",
    )
    builder.button(
        text="✅На что я уже подписался?)✅",
    )
    builder.button(
        text="💳Изменить реквизиты для перевода💳",
    )
    builder.button(
        text="¿?Вопросы и ответы¿?",
    )
    builder.adjust(1, 2, 1, 1)
    return builder.as_markup(resize_keyboard=True)