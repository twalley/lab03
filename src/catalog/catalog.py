from typing import Dict, Iterator, List

from .exceptions import DuplicateIdError, NotFoundError
from .models import AircraftPart


class Catalog:
    """
    Каталог авиационных деталей,
    использует словарь для быстрого поиска по ID,
    хранит детали в списке для сохранения порядка добавления.
    Порядок итерации: в порядке добавления деталей в каталог
    """

    def __init__(self):
        """Создание пустого каталога"""

        # словарь для быстрого поиска по ID
        self._items_by_id: Dict[str, AircraftPart] = {}

        # список для сохранения и итерации в порядке добавления
        self._items_list: List[AircraftPart] = []

    def add(self, item: AircraftPart) -> None:
        """Добавляет деталь в каталог"""

        if item.part_id in self._items_by_id:
            raise DuplicateIdError(f"Деталь с ID '{item.part_id}' уже существует")

        # добавляем в словарь для быстрого поиска по ID
        self._items_by_id[item.part_id] = item

        # добавляем в список для сохранения порядка добавления
        self._items_list.append(item)

    def get(self, item_id: str) -> AircraftPart:
        """Получает деталь по ID через словать"""

        if item_id not in self._items_by_id:
            raise NotFoundError(f"Деталь с ID '{item_id}' не найдена")

        # Возвращаем деталь из словаря
        return self._items_by_id[item_id]

    def remove(self, item_id: str) -> None:
        """
        Удаляет деталь из каталога,
        удаляет и из словаря, и из списка,
        чтобы они оставались согласованными
        """

        if item_id not in self._items_by_id:
            raise NotFoundError(f"Деталь с ID '{item_id}' не найдена")

        # получаем объект детали для удаления из списка
        item = self._items_by_id[item_id]

        # удаляем из словаря
        del self._items_by_id[item_id]

        # удаляем из списка
        self._items_list.remove(item)

    def find_by_category(self, category: str) -> List[AircraftPart]:
        """Ищет детали по категории, нужно пройти по всем деталям"""

        # создаём новый пустой список для результатов
        result: List[AircraftPart] = []

        # проходим по всем деталям в порядке добавления
        for item in self._items_list:
            # сравниваем категории чувствительно к регистру
            if item.category == category:
                result.append(item)

        # возвращаем копию списка, чтобы пользователь мог испортить каталог
        return result.copy()

    def find_by_name(self, query: str) -> List[AircraftPart]:
        """Ищет детали по названию не чувствителен к регистру,
        нужно пройти по всем деталям"""

        # приводим к нижнему регистру для сравнения
        query_lower = query.lower()

        # создаём новый пустой список для результатов
        result: List[AircraftPart] = []

        # проходим по всем деталям
        for item in self._items_list:
            # приводим название к нижнему регистру
            # проверяем, содержит ли оно запрос
            if query_lower in item.name.lower():
                result.append(item)

        # возвращаем копию списка
        return result.copy()

    def __len__(self) -> int:
        """
        Возвращает количество деталей в каталоге len(catalog)
        """
        return len(self._items_list)

    def __iter__(self) -> Iterator[AircraftPart]:
        """
        Итератор по деталям в порядке добавления
        for item in catalog:
        """
        # возвращаем итератор по списку сохраняя порядок добавления
        return iter(self._items_list)

    def __contains__(self, item_id: str) -> bool:
        """
        Проверяет, есть ли деталь с таким ID в каталоге
        if "ENG-001" in catalog:
        """
        return item_id in self._items_by_id
