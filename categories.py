"""Работа с категориями расходов"""
from typing import Dict, List, NamedTuple

from categories_list import categories_list


class Category(NamedTuple):
    """Структура категории"""

    codename: str
    name: str
    is_base_expense: bool
    aliases: List[str]


class Categories:
    """Класс категорий расходов"""

    def __init__(self):
        self._categories = self._load_categories()

    def _load_categories(self) -> List[Category]:
        """Возвращает справочник категорий расходов"""

        categories = [
            {
                "codename": cat[0],
                "name": cat[1],
                "is_base_expense": cat[2],
                "aliases": cat[3],
            }
            for cat in categories_list
        ]

        categories = self._fill_aliases(categories)
        return categories

    def _fill_aliases(self, categories: List[Dict]) -> List[Category]:
        """Заполняет по каждой категории aliases, то есть возможные
        названия этой категории, которые можем писать в тексте сообщения.
        Например, категория «кафе» может быть написана как cafe,
        ресторан и тд."""
        categories_result = []
        for _, category in enumerate(categories):
            aliases = category["aliases"].split(",")
            aliases = list(filter(None, map(str.strip, aliases)))
            aliases.append(category["codename"])
            aliases.append(category["name"])
            categories_result.append(
                Category(
                    codename=category["codename"],
                    name=category["name"],
                    is_base_expense=category["is_base_expense"],
                    aliases=aliases,
                )
            )
        return categories_result

    def get_all_categories(self) -> List[Dict]:
        """Возвращает справочник категорий."""
        return self._categories

    def get_category(self, category_name: str) -> Category:
        """Возвращает категорию по одному из её алиасов."""
        finded = None
        other_category = None
        for category in self._categories:
            if category.codename == "other":
                other_category = category
            for alias in category.aliases:
                if category_name == alias:
                    finded = category
        if not finded:
            finded = other_category
        return finded
