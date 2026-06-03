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

