import time
import pandas


class Validator:
    """
    _summary_
    """

    def __init__(self):
        pass

    @staticmethod
    def is_missing(value):
        return pandas.isna(value)

    @staticmethod
    def validate_date(value):
        if pandas.isna(value):
            return False

        if type(value) is str:
            try:
                time.strptime(value, "%d/%m/%Y")
                return True
            except ValueError:
                return False
        return False

    @staticmethod
    def validate_int(value):
        if pandas.isna(value):
            return False

        if type(value) is int:
            return True
        if type(value) is str:
            return value.isdigit()
        return False

    @staticmethod
    def validate_float(value):
        if pandas.isna(value):
            return False

        if type(value) is float:
            return True
        if type(value) is str:
            return value.replace(".", "").isdigit() and "." in value
        return False

    @staticmethod
    def validate_alpha(value):
        if pandas.isna(value):
            return False

        if type(value) is str:
            value = value.replace(" ", "")
            if value.isalpha():
                return True
            if value.replace("+", "").isalpha():
                return True
        return False

    @staticmethod
    def validate_bool(value):
        if pandas.isna(value):
            return False

        if type(value) is bool:
            return True
        if type(value) is str:
            return value == "True" or value == "False"
        return False

    def __str__(self):
        pass
