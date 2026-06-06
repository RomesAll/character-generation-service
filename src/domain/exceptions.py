class DomainException(Exception):
    def __init__(self,
                 message: str,
                 error_code: str | None = None,
                 details: dict | None = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)

    def __str__(self) -> str:
        if self.error_code:
            return f"{self.error_code}: {self.message}"
        return self.message

class InvalidReferenceException(DomainException):
    def __init__(self, reference: object, message: str):
        self.reference = reference
        self.message = message or (f'Неверный тип слабой ссылки, '
                                   f'ожидается объект weakref.ref, '
                                   f'передан: {reference}')
        super().__init__(
            message=self.message,
            error_code='WEAKREF-ERROR',
            details={'reference': self.reference}
        )

class PerkTypeException(DomainException):
    def __init__(self, invalid_attr_obj: object, message: str):
        self.invalid_attr_obj = invalid_attr_obj
        self.message = message or (f'Неверный тип атрибута, '
                                   f'ожидается объект Perk, '
                                   f'передан: {invalid_attr_obj}')
        super().__init__(
            message=self.message,
            error_code='PERK-ATTR-TYPE-ERROR'
        )

class StatEnumTypeException(DomainException):
    def __init__(self, invalid_attr_obj: object, message: str):
        self.invalid_attr_obj = invalid_attr_obj
        self.message = message or (f'Неверный тип атрибута, '
                                   f'ожидается объект StatEnum, '
                                   f'передан: {invalid_attr_obj}')
        super().__init__(
            message=self.message,
            error_code='STAT-ATTR-TYPE-ERROR'
        )

class MultiplierAmountTypeException(DomainException):
    def __init__(self, invalid_attr_obj: object, message: str):
        self.invalid_attr_obj = invalid_attr_obj
        self.message = message or (f'Неверный тип атрибута, '
                                   f'ожидается объект int, '
                                   f'передан: {invalid_attr_obj}')
        super().__init__(
            message=self.message,
            error_code='MULTIPLIER-AMOUNT-ATTR-TYPE-ERROR'
        )

class MeasurementTypeException(DomainException):
    def __init__(self, invalid_attr_obj: object, message: str):
        self.invalid_attr_obj = invalid_attr_obj
        self.message = message or (f'Неверный тип атрибута, '
                                   f'ожидается объект int, '
                                   f'передан: {invalid_attr_obj}')
        super().__init__(
            message=self.message,
            error_code='MEASUREMENT-ATTR-TYPE-ERROR'
        )

class NamePerkException(DomainException):
    def __init__(self, name_perk: object | str, message: str):
        self.message = message or ('Неверный тип атрибута, '
                                   'ожидается объект str, длина '
                                   'которой больше 2 но меньше 26')
        if type(name_perk) is str:
            self.message += f'. Передана строка {name_perk}, длина {len(name_perk)}'
        super().__init__(
            message=self.message,
            error_code='NAME-PERK-ATTR-ERROR'
        )

class PerkMultiplierException(DomainException):
    pass

class CurrentGreaterMaximumException(DomainException):
    pass

class DuplicateMultiplierException(DomainException):
    def __init__(self, multiplier):
        self.message = f'Модификатор {multiplier} уже содержится в стате'
        self.error_code = 'DUPLICATE-MULTIPLIER-STAT-ERROR'
        self.details = {
            'multiplier': multiplier,
        }
        super().__init__(self.message, self.error_code, self.details)

class NotFoundMultiplierException(DomainException):
    def __init__(self, multiplier):
        self.message = f'Модификатор {multiplier} уже найден'
        self.error_code = 'NOT-FOUND-MULTIPLIER-STAT-ERROR'
        self.details = {
            'multiplier': multiplier,
        }
        super().__init__(self.message, self.error_code, self.details)

class LevelException(DomainException):
    def __init__(self, level: int):
        self.message = f'Левел статов персонажа должен быть от 0 до 3, сейчас: {level}'
        self.error_code = 'LEVEL-ERROR'
        self.details = {
            'level': level,
        }
        super().__init__(self.message, self.error_code, self.details)

class DuplicatePerkException(DomainException):
    def __init__(self, perk_name: str):
        self.message = f'Перк {perk_name} уже содержится есть в коллекции'
        self.error_code = 'DUPLICATE-PERK-NAME-STAT-ERROR'
        self.details = {
            'perk_name': perk_name,
        }
        super().__init__(self.message, self.error_code, self.details)

class NotFoundPerkException(DomainException):
    def __init__(self, perk_name: str):
        self.message = f'Перк {perk_name} не найден'
        self.error_code = 'NOT-FOUND-PERK-NAME-STAT-ERROR'
        self.details = {
            'perk_name': perk_name,
        }
        super().__init__(self.message, self.error_code, self.details)

class BodyPartArmorException(DomainException):
    def __init__(self, new_armor: object, body_part_name: object):
        self.message = f'Броня {new_armor} не подходит по часть тела {body_part_name}'
        self.error_code = 'BODY-PART-ARMOR-ERROR'
        self.details = {
            'new_armor': new_armor,
            'body_part_name': body_part_name,
        }
        super().__init__(self.message, self.error_code, self.details)

class CharacterTypeException(DomainException):
    def __init__(self, message: str, error_type_object: object):
        self.message = message
        self.message += f'. Передан объект: {type(error_type_object)}'
        self.error_code = 'CHARACTER-TYPE-ERROR'
        self.details = {
            'error_type_object': error_type_object,
        }
        super().__init__(self.message, self.error_code, self.details)

class ImageFileException(DomainException):
    def __init__(self, image: object):
        self.message = f'Объект изображения {image} должен быть файлом'
        self.error_code = 'IMAGE-FILE-ERROR'
        self.details = {
            'image': image,
        }
        super().__init__(self.message, self.error_code, self.details)

class UnsupportedExtensionException(DomainException):
    def __init__(self, image: object):
        self.message = f'Объект изображения {image} должен быть файлом с расширением .png, .jpg, .webp'
        self.error_code = 'IMAGE-EXTENSION-FILE-ERROR'
        self.details = {
            'image': image,
        }
        super().__init__(self.message, self.error_code, self.details)

class FileNotFoundException(DomainException):
    def __init__(self, image: object):
        self.message = f'Объект изображения {image} не найден'
        self.error_code = 'IMAGE-NOT-FOUND-ERROR'
        self.details = {
            'image': image,
        }
        super().__init__(self.message, self.error_code, self.details)

class GroupStatsRefNotFoundException(DomainException):
    def __init__(self):
        self.message = 'Ссылка на group_stats не найдена'
        self.error_code = 'REF-FOUND-ERROR'
        super().__init__(self.message, self.error_code)