from enum import Enum

class ValidationError(Enum):
    EMPTY_LINE = "Поле не може бути порожнім"
    MIN_NAME = "Має містити не менше двох символів"
    NEGATIVE_AGE = "Вік не може бути від'ємним"
    UNDERAGE = "Для оренди спорядження і техніки клієнт має бути повнолітнім"
    INVALID_AGE_FORMAT = "Вік має бути числом"
    INVALID_NUMBER = "Номер має містити рівно 9 цифр"
    INVALID_EMAIL = "Некоректний формат електронної пошти"
    LONGER_PASSWORD = "Пароль має містити мінімум 8 символів"