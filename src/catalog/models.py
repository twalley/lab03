from dataclasses import dataclass

from .exceptions import InvalidEntityError


@dataclass
class AircraftPart:
    """Класс для представления авиационной детали"""

    # уникальный идентификатор
    part_id: str
    # название детали
    name: str
    # категория детали
    category: str
    # год производства
    year: int
    # производитель (дополнительное поле для авиационных деталей)
    manufacturer: str
    # вес в килограммах (дополнительное поле для авиационных деталей)
    weight_kg: float

    def __post_init__(self):
        """Метод вызывается после создания объекта.
        Здесь проверяем инварианты - правила, которые должны выполняться
        для любого валидного объекта"""

        if not self.part_id or not self.part_id.strip():
            raise InvalidEntityError("ID детали не может быть пустым")

        if not self.name or not self.name.strip():
            raise InvalidEntityError("Название детали не может быть пустым")

        if not self.category or not self.category.strip():
            raise InvalidEntityError("Категория не может быть пустой")

        if self.year < 1900 or self.year > 2026:
            raise InvalidEntityError(f"Год должен быть между 1900 и 2026, получен: {self.year}")

        if not self.manufacturer or not self.manufacturer.strip():
            raise InvalidEntityError("Производитель не может быть пустым")

        if self.weight_kg <= 0:
            raise InvalidEntityError(f"Вес должен быть положительным, получен: {self.weight_kg}")
