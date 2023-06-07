"""Сервер Telegram бота, запускаемый непосредственно"""
import logging
import os

from aiogram import Bot, Dispatcher, executor, types

import exceptions
import expenses
from categories import Categories
from middlewares import AccessMiddleware

logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
ACCESS_IDS = list(map(int, os.getenv("TELEGRAM_ACCESS_IDS").split(",")))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_IDS))


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """Отправляет приветственное сообщение и помощь по боту"""
    await message.answer(
        "Бот для учёта финансов\n\n"
        "Добавить расход: 250 такси\n"
        "Категории трат: /categories"
    )


@dp.message_handler(commands=["categories"])
async def categories_list(message: types.Message):
    """Отправляет список категорий расходов"""
    categories = Categories().get_all_categories()
    answer_message = "Категории трат:\n\n* " + (
        "\n* ".join([c.name + " (" + ", ".join(c.aliases) + ")" for c in categories])
    )
    await message.answer(answer_message)


@dp.message_handler()
async def add_expense_to_gs(message: types.Message):
    """Добавляет новый расход"""
    try:
        expense = expenses.add_expense_to_gs(message.text)
    except exceptions.NotCorrectMessage as exception:
        await message.answer(str(exception))
        return
    answer_message = f"Добавлены траты {expense.amount} руб на {expense.category_name}."
    await message.answer(answer_message)


if __name__ == "__main__":
    executor.start_polling(dp)
