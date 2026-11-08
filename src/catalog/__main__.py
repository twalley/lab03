from catalog import (
    AircraftPart,
    Catalog,
    DuplicateIdError,
    NotFoundError,
    load_catalog,
    save_catalog,
)


def main():
    # создаём каталог
    catalog = Catalog()

    # создаём детали
    part1 = AircraftPart(
        "ENG-001", "Турбовентиляторный двигатель", "двигатель", 2020, "Rolls-Royce", 2500.5
    )
    part2 = AircraftPart("WING-001", "Левое крыло", "крыло", 2019, "Boeing", 1200.0)
    part3 = AircraftPart(
        "ENG-002", "Турбовинтовой двигатель", "двигатель", 2021, "Pratt & Whitney", 1800.0
    )

    # добавляем в каталог
    catalog.add(part1)
    catalog.add(part2)
    catalog.add(part3)
    print(f"Добавлено деталей: {len(catalog)}")

    # проверяем наличие
    print(f"ENG-001 в каталоге: {'ENG-001' in catalog}")
    print(f"XXX в каталоге: {'XXX' in catalog}")

    # получаем по ID
    print(f"\nДеталь ENG-001: {catalog.get('ENG-001').name}")

    # ищем по категории
    print("\nДвигатели:")
    for p in catalog.find_by_category("двигатель"):
        print(f"  - {p.name}")

    # ищем по имени
    print("\nПоиск 'Турбо':")
    for p in catalog.find_by_name("Турбо"):
        print(f"  - {p.name}")

    # итерация
    print("\nВсе детали:")
    for p in catalog:
        print(f"  {p.part_id}: {p.name}")

    # сохраняем и загружаем
    save_catalog(catalog, "catalog.json")
    loaded = load_catalog("catalog.json")
    print(f"\nЗагружено из файла: {len(loaded)} деталей")

    # удаляем
    catalog.remove("WING-001")
    print(f"\nПосле удаления WING-001: {len(catalog)} деталей")

    # проверяем ошибки
    try:
        catalog.remove("XXX")
    except NotFoundError as er:
        print(f"Ошибка удаления: {er}")

    try:
        catalog.add(part1)
    except DuplicateIdError as er:
        print(f"Ошибка дубликата: {er}")


if __name__ == "__main__":
    main()
