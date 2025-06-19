import re

from django.core.exceptions import ValidationError


class SymbolValidator:
    def validate(self, password, user=None):
        if not re.search(r"[^\w\s]", password):
            raise ValidationError("Password must contain atleast one special character")
