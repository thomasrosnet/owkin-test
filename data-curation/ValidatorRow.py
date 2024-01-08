import pandas
import time
from Validator import Validator



class ValidatorRow(Validator):

    row_index = ""
    df_row = ""
    col_name_type = ""
    nb_missing = ""
    nb_valid = int
    nb_invalid = int
    is_row_valid = bool
    invalid_values = {}
    row_threshold = 0.1

    row_quality = {}

    def __init__(self, row_index, df_row, col_name_type):
        self.row_index = row_index
        self.df_row = df_row
        self.col_name_type = col_name_type

        # Count missing values in the row
        self.nb_missing = int(self.df_row.apply(super().is_missing).sum())
        self.nb_columns = len(df_row)


        self.validate_row()
        self.calculate_rates()
        self.is_row_valid()
        self.row_quality()


    def validate_row(self):
        nb_valid = 0
        nb_invalid = 0
        invalid_values = {}
        for col_name in self.col_name_type.keys():
            
            # Call validate methods here
            match self.col_name_type[col_name]:
                case "Date":
                    is_valid = super().validate_date(self.df_row[col_name])
                case "Int":
                    is_valid = super().validate_int(self.df_row[col_name])
                case "Float":
                    is_valid = super().validate_float(self.df_row[col_name])
                case "Alpha":
                    is_valid = super().validate_alpha(self.df_row[col_name])
                case "Boolean":
                    is_valid = super().validate_bool(self.df_row[col_name])
            if is_valid:
                nb_valid += 1
            else:
                nb_invalid += 1
                invalid_values[col_name] = self.df_row[col_name]


        self.nb_valid = nb_valid
        self.nb_invalid = nb_invalid - self.nb_missing
        self.invalid_values = invalid_values


        # self.row_quality[self.row_index] = row_summary

    def calculate_rates(self):
        self.rate_valid = round(self.nb_valid / self.nb_columns, 4)
        self.rate_invalid = round(self.nb_invalid / self.nb_columns, 4)
        self.rate_missing = round(self.nb_missing / self.nb_columns, 4)

    def is_row_valid(self):
        self.is_row_valid = bool(self.rate_valid > 1 - self.row_threshold)
        
    def row_quality(self):
        self.row_quality = {
            "nb_valid": self.nb_valid,
            "nb_invalid": self.nb_invalid,
            "nb_missing": self.nb_missing,
            "rate_valid": self.rate_valid,
            "rate_invalid": self.rate_invalid,
            "rate_missing": self.rate_missing,
            "row_threshold": self.row_threshold,
            "is_row_valid": self.is_row_valid,
            "invalid_values": self.invalid_values
        }

    def get_is_row_valid(self):
        return self.is_row_valid

    def get_row_quality(self):
        return self.row_quality
    