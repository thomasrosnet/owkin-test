import pandas
import time
import datetime
import copy
from Validator import Validator

class ValidatorCol(Validator):
    """
    _summary_
    """

    df_column = ""
    df_column_name = ""

    date_score = ""
    int_score = ""
    float_score = ""
    alpha_score = ""
    bool_score = ""

    guessed_type = ""
    max_score = ""
    invalid_miss = ""
    nb_valid = ""
    nb_missing = ""
    nb_invalid = ""
    invalid = ""
    score_summary = ""
    types_summary = {}

    alpha_unique = []
    column_describe = {}

    def __init__(self, df_column):
        self.df_column = df_column
        self.df_column_name = df_column.name


        # Count missing values in the colum
        self.nb_missing = int(self.df_column.apply(super().is_missing).sum())

        # Check number of conform value for each type
        self.date_score = int(self.df_column.apply(super().validate_date).sum())
        self.int_score = int(self.df_column.apply(super().validate_int).sum())
        self.float_score = int(self.df_column.apply(super().validate_float).sum())
        self.alpha_score = int(self.df_column.apply(super().validate_alpha).sum())
        self.bool_score = int(self.df_column.apply(super().validate_bool).sum())

        # Check which type is the best match
        self.guess_type()

        # count and list incorrect values
        self.count_invalid()
        self.count_valid()
        self.select_invalid()

        self.def_describe_column_on_type()

        self.column_quality()





    def select_missing(self):
        pass

    def select_invalid(self):
        match self.guessed_type:
            case "Date":
                self.invalid = self.df_column[~self.df_column.apply(super().validate_date)].to_dict()
            case "Int":
                self.invalid = self.df_column[~self.df_column.apply(super().validate_int)].to_dict()
            case "Float":
                self.invalid = self.df_column[~self.df_column.apply(super().validate_float)].to_dict()
            case "Alpha":
                self.invalid = self.df_column[~self.df_column.apply(super().validate_alpha)].to_dict()
            case "Boolean":
                self.invalid = self.df_column[~self.df_column.apply(super().validate_bool)].to_dict()


    def guess_type(self):
        types_summary = {
            "Date": self.date_score,
            "Int": self.int_score,
            "Float": self.float_score,
            "Alpha": self.alpha_score,
            "Boolean": self.bool_score,
        }

        self.guessed_type = max(types_summary, key=types_summary.get)
        self.max_score = types_summary[self.guessed_type]
        self.invalid_miss = len(self.df_column) - self.max_score

        # do something with it
        types_summary["Type"] = self.guessed_type
        self.types_summary = types_summary

        # try describe col depending of its type
        if self.guessed_type == "Alpha":
            self.alpha_unique = self.df_column.unique().tolist()

        # print(self.column_describe)

    
    def count_invalid(self):
        self.nb_invalid = self.invalid_miss - self.nb_missing
        #TODO add incorrect %

    def count_valid(self):
        self.nb_valid = len(self.df_column) - self.invalid_miss

    def replace_invalid_NA(self):
        self.df_column_describe = copy.deepcopy(self.df_column)
        for index in self.invalid.keys():
            self.df_column_describe[index] = pandas.NA

    def def_describe_column_on_type(self):
        self.replace_invalid_NA()
        # print(self.df_column)

        describe = {}
        match self.guessed_type:
            case "Date":
                # self.df_column_describe = pandas.to_datetime(self.df_column_describe, format="%d/%m/%Y")
                pass
            case "Int":
                # self.df_column_describe.astype = self.df_column_describe.astype(pandas.Int64Dtype())
                self.df_column_describe = pandas.to_numeric(self.df_column_describe)
            case "Float":
                # self.df_column_describe.astype = self.df_column_describe.astype(pandas.Float64Dtype())
                self.df_column_describe = pandas.to_numeric(self.df_column_describe)
            case "Alpha":
                self.df_column_describe.astype = self.df_column_describe.astype(pandas.StringDtype())
            case "Boolean":
                self.df_column_describe.astype = self.df_column_describe.astype(bool)

        # if self.guessed_type == "Date":
        #     desc = self.df_column_describe.describe().to_dict()
        #     for key in desc.keys():
        #         # print(type(desc[key]))
        #         # if type(describe[key]) == Timestap
        #         try:
        #             desc[key] = datetime.datetime.strptime(str(desc[key]), '%Y-%m-%d %H:%M:%S').strftime("%d/%m/%Y")
        #         except ValueError as e:
        #             # print(e)
        #             continue
        #         try:
        #             desc[key] = datetime.datetime.strptime(str(desc[key]), '%Y-%m-%d %H:%M:%S.%f').strftime("%d/%m/%Y")
        #         except ValueError as e:
        #             # print(e)
        #             continue                
        #     self.column_describe = desc
        # else:
        self.column_describe = self.df_column_describe.describe().to_dict()


    #TODO write the column summary in dict format
    def column_quality(self):

        column_quality = {
            "type_guess": self.types_summary,
            "nb_valid": self.nb_valid,
            "nb_missing": self.nb_missing,
            "nb_invalid": self.nb_invalid,
            "invalid_values": self.invalid,
            "unique": self.alpha_unique,
            "describe": self.column_describe
        }

        self.column_quality = column_quality


    def get_date_score(self):
        return self.date_score

    def get_int_score(self):
        return self.int_score

    def get_float_score(self):
        return self.float_score

    def get_alpha_score(self):
        return self.alpha_score

    def get_bool_score(self):
        return self.bool_score

    def get_nb_valid(self):
        return self.nb_valid

    def get_nb_invalid(self):
        return self.nb_invalid

    def get_nb_missing(self):
        return self.nb_missing

    def get_guessed_type(self):
        return self.guessed_type

    def get_max_score(self):
        return self.max_score

    def get_invalid_miss(self):
        return self.invalid_miss
    
    def get_invalid(self):
        return self.get_invalid
    
    def get_types_summary(self):
        return self.types_summary
    
    def get_column_quality(self):
        return self.column_quality

    def __str__(self):
        str = f"{self.df_column_name}:\t {self.guessed_type} | {self.max_score} | {self.nb_invalid} | {self.nb_missing}"
        return str