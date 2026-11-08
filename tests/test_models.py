import unittest

from catalog import AircraftPart, InvalidEntityError


class TestAircraftPart(unittest.TestCase):
    """Тесты для класса AircraftPart"""

    def test_valid_part_creation(self):
        """Тест создания валидной детали"""
        # создаём валидную деталь со всеми полями
        part = AircraftPart(
            part_id="ENG-001",
            name="Турбовентиляторный двигатель",
            category="двигатель",
            year=2020,
            manufacturer="Rolls-Royce",
            weight_kg=2500.5,
        )

        # проверяем, что все поля установлены правильно
        self.assertEqual(part.part_id, "ENG-001")
        self.assertEqual(part.name, "Турбовентиляторный двигатель")
        self.assertEqual(part.category, "двигатель")
        self.assertEqual(part.year, 2020)
        self.assertEqual(part.manufacturer, "Rolls-Royce")
        self.assertEqual(part.weight_kg, 2500.5)

    def test_empty_part_id_raises_error(self):
        """Тест что пустой ID вызывает ошибку"""
        with self.assertRaises(InvalidEntityError):
            AircraftPart(
                part_id="",
                name="Двигатель",
                category="двигатель",
                year=2020,
                manufacturer="Rolls-Royce",
                weight_kg=2500.0,
            )

    def test_whitespace_part_id_raises_error(self):
        """Тест что ID из пробелов вызывает ошибку"""
        with self.assertRaises(InvalidEntityError):
            AircraftPart(
                part_id="   ",
                name="Двигатель",
                category="двигатель",
                year=2020,
                manufacturer="Rolls-Royce",
                weight_kg=2500.0,
            )

    def test_empty_name_raises_error(self):
        """Тест что пустое название вызывает ошибку"""
        with self.assertRaises(InvalidEntityError):
            AircraftPart(
                part_id="ENG-001",
                name="",
                category="двигатель",
                year=2020,
                manufacturer="Rolls-Royce",
                weight_kg=2500.0,
            )

    def test_empty_category_raises_error(self):
        """Тест что пустая категория вызывает ошибку"""
        with self.assertRaises(InvalidEntityError):
            AircraftPart(
                part_id="ENG-001",
                name="Двигатель",
                category="",
                year=2020,
                manufacturer="Rolls-Royce",
                weight_kg=2500.0,
            )

    def test_invalid_year_too_old(self):
        """Тест что слишком старый год вызывает ошибку"""
        with self.assertRaises(InvalidEntityError):
            AircraftPart(
                part_id="ENG-001",
                name="Двигатель",
                category="двигатель",
                year=1800,
                manufacturer="Rolls-Royce",
                weight_kg=2500.0,
            )

    def test_invalid_year_too_new(self):
        """Тест что слишком новый год вызывает ошибку"""
        with self.assertRaises(InvalidEntityError):
            AircraftPart(
                part_id="ENG-001",
                name="Двигатель",
                category="двигатель",
                year=2100,
                manufacturer="Rolls-Royce",
                weight_kg=2500.0,
            )

    def test_empty_manufacturer_raises_error(self):
        """Тест что пустой производитель вызывает ошибку"""
        with self.assertRaises(InvalidEntityError):
            AircraftPart(
                part_id="ENG-001",
                name="Двигатель",
                category="двигатель",
                year=2020,
                manufacturer="",
                weight_kg=2500.0,
            )

    def test_negative_weight_raises_error(self):
        """Тест что отрицательный вес вызывает ошибку"""
        with self.assertRaises(InvalidEntityError):
            AircraftPart(
                part_id="ENG-001",
                name="Двигатель",
                category="двигатель",
                year=2020,
                manufacturer="Rolls-Royce",
                weight_kg=-100.0,
            )

    def test_zero_weight_raises_error(self):
        """Тест что нулевой вес вызывает ошибку"""
        with self.assertRaises(InvalidEntityError):
            AircraftPart(
                part_id="ENG-001",
                name="Двигатель",
                category="двигатель",
                year=2020,
                manufacturer="Rolls-Royce",
                weight_kg=0.0,
            )


if __name__ == "__main__":
    unittest.main()
