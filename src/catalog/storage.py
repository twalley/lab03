import json

from .catalog import Catalog
from .exceptions import CorruptedFileError, InvalidEntityError, UnsupportedVersionError
from .models import AircraftPart

# если добавим новое поле в AircraftPart, увеличим версию до 2
CURRENT_FORMAT_VERSION = 1


def save_catalog(catalog: Catalog, filepath: str) -> None:
    """Сохраняет каталог в JSON файл"""

    # создаём словарь данных для JSON
    data = {
        "format_version": CURRENT_FORMAT_VERSION,
        "items": [],
    }

    # проходим по всем деталям в каталоге в порядке добавления
    for item in catalog:
        # преобразуем каждую деталь в словарь
        item_dict = {
            "part_id": item.part_id,
            "name": item.name,
            "category": item.category,
            "year": item.year,
            "manufacturer": item.manufacturer,
            "weight_kg": item.weight_kg,
        }
        data["items"].append(item_dict)

    # открываем файл для записи в режиме записи ("w")
    # encoding="utf-8" нужен для корректной работы с русским текстом
    with open(filepath, "w", encoding="utf-8") as f:
        # pаписываем JSON с отступами (indent=2) для читаемости
        # ensure_ascii=False чтобы русские буквы не превращались в \uXXXX
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_catalog(filepath: str) -> Catalog:
    """Загружает каталог из JSON файла, если произошла ошибка,
    существующий каталог не изменяется"""

    # читаем файл
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

    except json.JSONDecodeError as er:
        raise CorruptedFileError(f"Файл содержит некорректный JSON: {er}")

    except FileNotFoundError:
        raise CorruptedFileError(f"Файл не найден: {filepath}")

    if not isinstance(data, dict):
        raise CorruptedFileError("Корневой элемент должен быть словарём")

    if "format_version" not in data:
        raise CorruptedFileError("Отсутствует поле format_version")

    if data["format_version"] != CURRENT_FORMAT_VERSION:
        raise UnsupportedVersionError(
            f"Неподдерживаемая версия формата: {data['format_version']}."
            f"Ожидается: {CURRENT_FORMAT_VERSION}"
        )

    if "items" not in data:
        raise CorruptedFileError("Отсутствует поле items")

    # проверяем, что это список
    if not isinstance(data["items"], list):
        raise CorruptedFileError("Поле items должно быть списком")

    # создаём новый каталог, не изменяем существующий
    new_catalog = Catalog()

    # загружаем все детали в новый каталог
    for i, item_data in enumerate(data["items"]):
        try:
            # проверяем, что это словарь
            if not isinstance(item_data, dict):
                raise CorruptedFileError(f"Элемент {i} не является словарём")

            # проверяем наличие всех необходимых полей
            required_fields = ["part_id", "name", "category", "year", "manufacturer", "weight_kg"]
            for field in required_fields:
                if field not in item_data:
                    raise CorruptedFileError(f"В элементе {i} отсутствует поле {field}")

            # создаём деталь, конструктор проверит инварианты
            part = AircraftPart(
                part_id=item_data["part_id"],
                name=item_data["name"],
                category=item_data["category"],
                year=item_data["year"],
                manufacturer=item_data["manufacturer"],
                weight_kg=item_data["weight_kg"],
            )

            # добавляем в новый каталог
            new_catalog.add(part)

        except InvalidEntityError as er:
            raise CorruptedFileError(f"Невалидная деталь в элементе {i}: {er}")

    return new_catalog
