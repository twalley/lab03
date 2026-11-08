import unittest

from catalog import AircraftPart, Catalog, DuplicateIdError, NotFoundError


class TestCatalog(unittest.TestCase):
    """Тесты для класса Catalog"""

    def setUp(self):
        """
        Метод вызывается перед каждым тестом.
        Здесь создаём свежий каталог и тестовые детали
        """
        self.catalog = Catalog()

        # создаём три тестовые детали
        self.part1 = AircraftPart(
            part_id="ENG-001",
            name="Турбовентиляторный двигатель",
            category="двигатель",
            year=2020,
            manufacturer="Rolls-Royce",
            weight_kg=2500.5,
        )

        self.part2 = AircraftPart(
            part_id="WING-001",
            name="Левое крыло",
            category="крыло",
            year=2019,
            manufacturer="Boeing",
            weight_kg=1200.0,
        )

        self.part3 = AircraftPart(
            part_id="ENG-002",
            name="Турбовинтовой двигатель",
            category="двигатель",
            year=2021,
            manufacturer="Pratt & Whitney",
            weight_kg=1800.0,
        )

    def test_add_and_get(self):
        """Тест добавления и получения детали"""
        # добавляем деталь
        self.catalog.add(self.part1)

        # получаем деталь по ID
        retrieved = self.catalog.get("ENG-001")

        # проверяем, что это та же деталь
        self.assertEqual(retrieved.part_id, "ENG-001")
        self.assertEqual(retrieved.name, "Турбовентиляторный двигатель")

    def test_add_duplicate_raises_error(self):
        """Тест что дубликат ID вызывает ошибку"""
        # добавляем первую деталь
        self.catalog.add(self.part1)

        # создаём деталь с таким же ID
        duplicate = AircraftPart(
            part_id="ENG-001",
            name="Другой двигатель",
            category="двигатель",
            year=2022,
            manufacturer="GE",
            weight_kg=3000.0,
        )

        # пытаемся добавить дубликат, должна быть ошибка
        with self.assertRaises(DuplicateIdError):
            self.catalog.add(duplicate)

    def test_get_nonexistent_raises_error(self):
        """Тест что получение несуществующей детали вызывает ошибку"""
        with self.assertRaises(NotFoundError):
            self.catalog.get("NONEXISTENT")

    def test_remove(self):
        """Тест удаления детали"""
        # добавляем деталь
        self.catalog.add(self.part1)

        # проверяем, что она есть
        self.assertIn("ENG-001", self.catalog)

        # удаляем деталь
        self.catalog.remove("ENG-001")

        # проверяем, что её больше нет
        self.assertNotIn("ENG-001", self.catalog)
        self.assertEqual(len(self.catalog), 0)

    def test_remove_nonexistent_raises_error(self):
        """Тест что удаление несуществующей детали вызывает ошибку"""
        with self.assertRaises(NotFoundError):
            self.catalog.remove("NONEXISTENT")

    def test_len(self):
        """Тест метода __len__"""
        # пустой каталог
        self.assertEqual(len(self.catalog), 0)

        # добавляем детали
        self.catalog.add(self.part1)
        self.assertEqual(len(self.catalog), 1)

        self.catalog.add(self.part2)
        self.assertEqual(len(self.catalog), 2)

        # удаляем деталь
        self.catalog.remove("ENG-001")
        self.assertEqual(len(self.catalog), 1)

    def test_contains(self):
        """Тест метода __contains__"""
        # добавляем деталь
        self.catalog.add(self.part1)

        # проверяем наличие
        self.assertIn("ENG-001", self.catalog)
        self.assertNotIn("ENG-002", self.catalog)

    def test_iter(self):
        """Тест итерации по каталогу"""
        # добавляем детали в определённом порядке
        self.catalog.add(self.part1)
        self.catalog.add(self.part2)
        self.catalog.add(self.part3)

        # получаем список деталей через итерацию
        items = list(self.catalog)

        # проверяем порядок, должен быть порядок добавления
        self.assertEqual(len(items), 3)
        self.assertEqual(items[0].part_id, "ENG-001")
        self.assertEqual(items[1].part_id, "WING-001")
        self.assertEqual(items[2].part_id, "ENG-002")

    def test_iter_twice_gives_same_order(self):
        """Тест что итерация дважды даёт одинаковый порядок"""
        self.catalog.add(self.part1)
        self.catalog.add(self.part2)

        first_run = list(self.catalog)
        second_run = list(self.catalog)

        self.assertEqual(first_run, second_run)

    def test_find_by_category(self):
        """Тест поиска по категории"""
        # добавляем детали
        self.catalog.add(self.part1)
        self.catalog.add(self.part2)
        self.catalog.add(self.part3)

        # ищем двигатели
        engines = self.catalog.find_by_category("двигатель")

        # проверяем результат
        self.assertEqual(len(engines), 2)
        self.assertEqual(engines[0].part_id, "ENG-001")
        self.assertEqual(engines[1].part_id, "ENG-002")

        # ищем крылья
        wings = self.catalog.find_by_category("крыло")
        self.assertEqual(len(wings), 1)
        self.assertEqual(wings[0].part_id, "WING-001")

        # ищем несуществующую категорию
        empty = self.catalog.find_by_category("шасси")
        self.assertEqual(len(empty), 0)

    def test_find_by_name_case_insensitive(self):
        """Тест что поиск по имени не чувствителен к регистру"""
        # добавляем детали
        self.catalog.add(self.part1)
        self.catalog.add(self.part2)
        self.catalog.add(self.part3)

        # ищем с разным регистром
        result1 = self.catalog.find_by_name("двигатель")
        result2 = self.catalog.find_by_name("ДВИГАТЕЛЬ")
        result3 = self.catalog.find_by_name("Двигатель")

        # все результаты должны быть одинаковыми
        self.assertEqual(len(result1), 2)
        self.assertEqual(len(result2), 2)
        self.assertEqual(len(result3), 2)

    def test_find_by_name_partial_match(self):
        """Тест частичного совпадения в поиске по имени"""
        # добавляем детали (part1 и part3 обе содержат "Турбо")
        self.catalog.add(self.part1)
        self.catalog.add(self.part3)  # было part2, стало part3
        # ищем по части названия
        result = self.catalog.find_by_name("Турбо")
        # должны найти обе детали (обе содержат "Турбо")
        self.assertEqual(len(result), 2)

    def test_find_returns_copy(self):
        """Тест что поиск возвращает копию, а не внутренний список"""
        # добавляем детали
        self.catalog.add(self.part1)
        self.catalog.add(self.part2)

        # получаем результат поиска
        result = self.catalog.find_by_category("двигатель")

        # пытаемся изменить результат
        result.clear()

        # проверяем, что каталог не изменился
        self.assertEqual(len(self.catalog), 2)


# эта конструкция нужна, чтобы тесты можно было запускать напрямую
if __name__ == "__main__":
    unittest.main()
