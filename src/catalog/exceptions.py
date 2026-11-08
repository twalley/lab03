class CatalogError(Exception):
    """Базовое исключение для операций с каталогом"""

    pass


class InvalidEntityError(CatalogError):
    """Ошибка при создании невалидной сущности"""

    pass


class DuplicateIdError(CatalogError):
    """Ошибка при попытке добавить дубликат ID"""

    pass


class NotFoundError(CatalogError):
    """Ошибка когда объект не найден"""

    pass


class UnsupportedVersionError(CatalogError):
    """Ошибка при неподдерживаемой версии формата"""

    pass


class CorruptedFileError(CatalogError):
    """Ошибка при повреждённом файле"""

    pass
