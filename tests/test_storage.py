import json
import os
import tempfile
import unittest

from catalog import (
    AircraftPart,
    Catalog,
    CorruptedFileError,
    UnsupportedVersionError,
    load_catalog,
    save_catalog,
)


class TestStorage(unittest.TestCase):
    """Тесты для сохранения и загрузки каталога"""

    def setUp(self):
        """Создаём временный файл для тестов"""
        # создаём временный файл
        self.temp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
        self.temp_file.close()
        self.filepath = self.temp_file.name

        # создаём тестовый каталог с двумя деталями
        self.catalog = Catalog()
        self.catalog.add(
            AircraftPart(
                part_id="ENG-001",
                name="Турбовентиляторный двигатель",
                category="двигатель",
                year=2020,
                manufacturer="Rolls-Royce",
                weight_kg=2500.5,
            )
        )
        self.catalog.add(
            AircraftPart(
                part_id="WING-001",
                name="Левое крыло",
                category="крыло",
                year=2019,
                manufacturer="Boeing",
                weight_kg=1200.0,
            )
        )

    def tearDown(self):
        """Удаляем временный файл после теста"""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)

    def test_save_and_load_round_trip(self):
        """Тест сохранения и загрузки (round trip)"""
        # сохраняем каталог
        save_catalog(self.catalog, self.filepath)

        # загружаем каталог
        loaded_catalog = load_catalog(self.filepath)

        # проверяем, что количество деталей совпадает
        self.assertEqual(len(loaded_catalog), len(self.catalog))

        # проверяем каждую деталь
        for original_item in self.catalog:
            loaded_item = loaded_catalog.get(original_item.part_id)

            # проверяем все поля
            self.assertEqual(loaded_item.part_id, original_item.part_id)
            self.assertEqual(loaded_item.name, original_item.name)
            self.assertEqual(loaded_item.category, original_item.category)
            self.assertEqual(loaded_item.year, original_item.year)
            self.assertEqual(loaded_item.manufacturer, original_item.manufacturer)
            self.assertEqual(loaded_item.weight_kg, original_item.weight_kg)

    def test_load_with_unsupported_version(self):
        """Тест загрузки с неподдерживаемой версией"""
        data = {
            "format_version": 999,
            "items": [],
        }

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)

        # пытаемся загрузить, должна быть ошибка
        with self.assertRaises(UnsupportedVersionError):
            load_catalog(self.filepath)

    def test_load_with_corrupted_json(self):
        """Тест загрузки повреждённого JSON"""
        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write("{invalid json")

        # пытаемся загрузить, должна быть ошибка
        with self.assertRaises(CorruptedFileError):
            load_catalog(self.filepath)

    def test_load_with_missing_fields(self):
        """Тест загрузки с отсутствующими полями"""
        data = {
            "format_version": 1,
            "items": [
                {
                    "part_id": "ENG-001"
                    # отсутствуют другие поля
                }
            ],
        }

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)

        # пытаемся загрузить, должна быть ошибка
        with self.assertRaises(CorruptedFileError):
            load_catalog(self.filepath)

    def test_atomic_load_on_error(self):
        """Тест атомарности загрузки при ошибке"""
        # создаём каталог с одной деталью
        original_catalog = Catalog()
        original_catalog.add(
            AircraftPart(
                part_id="ORIGINAL-001",
                name="Оригинальная деталь",
                category="тест",
                year=2020,
                manufacturer="Test",
                weight_kg=100.0,
            )
        )

        # создаём JSON с валидной и невалидной деталью
        data = {
            "format_version": 1,
            "items": [
                {
                    "part_id": "VALID-001",
                    "name": "Валидная деталь",
                    "category": "тест",
                    "year": 2020,
                    "manufacturer": "Test",
                    "weight_kg": 100.0,
                },
                {
                    "part_id": "",
                    "name": "Невалидная деталь",
                    "category": "тест",
                    "year": 2020,
                    "manufacturer": "Test",
                    "weight_kg": 100.0,
                },
            ],
        }

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f)

        # пытаемся загрузить, должна быть ошибка
        with self.assertRaises(CorruptedFileError):
            load_catalog(self.filepath)

        # проверяем, что оригинальный каталог не изменился
        self.assertEqual(len(original_catalog), 1)
        self.assertIn("ORIGINAL-001", original_catalog)

    def test_save_preserves_all_fields(self):
        """Тест что сохранение сохраняет все поля"""
        # сохраняем каталог
        save_catalog(self.catalog, self.filepath)

        # читаем JSON напрямую
        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # проверяем структуру
        self.assertIn("format_version", data)
        self.assertIn("items", data)
        self.assertEqual(len(data["items"]), 2)

        # проверяем первую деталь
        item1 = data["items"][0]
        self.assertIn("part_id", item1)
        self.assertIn("name", item1)
        self.assertIn("category", item1)
        self.assertIn("year", item1)
        self.assertIn("manufacturer", item1)
        self.assertIn("weight_kg", item1)


if __name__ == "__main__":
    unittest.main()
