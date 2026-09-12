import re
from constants import ValidationError

class Validation:
    def __init__(self, name: str, age: str, number: str, email: str, password: str):
        self.name = name
        self.age = age
        self.number = number
        self.email = email
        self.password = password

    def audit_name(self):
        if not self.name:
            return ValidationError.EMPTY_LINE
        if len(self.name) < 2:
            return ValidationError.MIN_NAME
        return None

    def audit_age(self):
        if not self.age :
            return ValidationError.EMPTY_LINE
        if not self.age.isdigit():
            return ValidationError.INVALID_AGE_FORMAT

        age_int = int(self.age)
        if age_int < 0:
            return ValidationError.NEGATIVE_AGE
        if age_int < 18:
            return ValidationError.UNDERAGE
        return None

    def audit_number(self):
        if not self.number:
            return ValidationError.EMPTY_LINE
        if len(self.number) != 9 or not self.number.isdigit():
            return ValidationError.INVALID_NUMBER
        return None

    def audit_email(self):
        if not self.email:
            return ValidationError.EMPTY_LINE

        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.fullmatch(pattern, self.email):
            return ValidationError.INVALID_EMAIL
        return None

    def audit_password(self):
        if not self.password:
            return ValidationError.EMPTY_LINE
        if len(self.password) < 8:
            return ValidationError.LONGER_PASSWORD
        return None

    def run_all_audits(self):
        errors = {}
        if error := self.audit_name():
            errors["name"] = error.value
        if error := self.audit_age():
            errors["age"] = error.value
        if error := self.audit_number():
            errors["number"] = error.value
        if error := self.audit_email():
            errors["email"] = error.value
        if error := self.audit_password():
            errors["password"] = error.value
        return errors

