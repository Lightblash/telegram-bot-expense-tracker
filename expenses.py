""" Работа с расходами"""
import base64
import datetime
import os
import re
from typing import NamedTuple, Optional

import pytz
from dotenv import load_dotenv

import exceptions
from categories import Categories
from gsheets import get_spreadsheet
from helpers import get_env_var

# Load environment variables from .env file
load_dotenv()

encoded_service_acc_info = os.environ["GOOGLE_SERVICE_ACCOUNT"]
client_secret = base64.b64decode(encoded_service_acc_info).decode()
GS_TITLE = get_env_var("GOOGLE_SPREADSHEET_TITLE")
WS_TITLE = get_env_var("GOOGLE_WORKSHEET_TITLE")


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""

    amount: int
    category_text: str


class Expense(NamedTuple):
    """Структура добавленного нового расхода"""

    id: Optional[int]
    amount: int
    category_name: str


def add_expense_to_gs(raw_message: str) -> Expense:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(parsed_message.category_text)

    row_exp_json = [
        _get_now_formatted(),
        category.name,
        parsed_message.amount,
        category.is_base_expense,
    ]
    spreadsheet = get_spreadsheet(client_secret, GS_TITLE)
    sheet = spreadsheet.worksheet(WS_TITLE)
    index = 2
    sheet.insert_row(row_exp_json, index, value_input_option="USER_ENTERED")
    return Expense(id=None, amount=parsed_message.amount, category_name=category.name)


def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if (
        not regexp_result
        or not regexp_result.group(0)
        or not regexp_result.group(1)
        or not regexp_result.group(2)
    ):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n1500 метро"
        )

    amount = regexp_result.group(1).replace(" ", "")
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    timezone = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(timezone)
    return now
