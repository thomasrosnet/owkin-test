import time
import pandas


class Validator:
    """
    _summary_
    """

    df_column = ""

    date_score = ""
    int_score = ""
    float_score = ""
    alpha_score = ""
    bool_score = ""

    guessed_type = ""
    max_score = ""
    incorrect_miss = ""
    score_summary = ""

    alpha_unique = []
    int_stats = {}
    float_stats = {}

    def __init__(self, df_column):
        self.df_column = df_column

        self.date_score = self.df_column.apply(self.validate_date).sum()
        self.int_score = self.df_column.apply(self.validate_int).sum()
        self.float_score = self.df_column.apply(self.validate_float).sum()
        self.alpha_score = self.df_column.apply(self.validate_alpha).sum()
        self.bool_score = self.df_column.apply(self.validate_bool).sum()

        self.score_summary()

    def columns_parser(self):
        pass

    def score_summary(self):
        summary = {
            "Date": self.date_score,
            "Int": self.int_score,
            "Float": self.float_score,
            "Alpha": self.alpha_score,
            "Boolean": self.bool_score,
        }

        self.guessed_type = max(summary, key=summary.get)
        self.max_score = summary[self.guessed_type]
        self.incorrect_miss = len(self.df_column) - self.max_score

        # do somzthing with it
        summary["Type"] = self.guessed_type

        self.score_summary = summary

        if self.guessed_type == "Alpha":
            self.alpha_unique = self.df_column.unique()

        if self.guessed_type == "Int":
            self.int_stats = self.df_column.describe().to_dict()

        if self.guessed_type == "Float":
            self.float_stats = self.df_column.describe().to_dict()

    def validate_date(self, value):
        # date = input('Date (mm/dd/yyyy): ')
        if type(value) is str:
            try:
                time.strptime(value, "%d/%m/%Y")
                return True
            except ValueError:
                return False
        return False

    def validate_int(self, value):
        if type(value) is int:
            return True
        if type(value) is str:
            return value.isdigit()
        return False

    def validate_float(self, value):
        if type(value) is float:
            return True
        if type(value) is str:
            return value.replace(".", "").isdigit() and "." in value
        return False

    def validate_alpha(self, value):
        if type(value) is str:
            if value.isalpha():
                return True
            if value.replace("+", "").isalpha():
                return True
        return False

    def validate_bool(self, value):
        if type(value) is bool:
            return True
        if type(value) is str:
            return value == "True" or value == "False"
        return False

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

    def get_guessed_type(self):
        return self.guessed_type

    def get_max_score(self):
        return self.max_score

    def get_incorrect_miss(self):
        return self.incorrect_miss

    def __str__(self):
        str = f"{self.guessed_type} | {self.max_score} | {self.incorrect_miss}"
        return str

    # def guess_types_from_df(self, df):
    #     # For each main type, define a lambda helper function which returns the number of values in the given column of said type
    #     helpers = {
    #         "float": lambda df, col: df[col]
    #         .apply(lambda x: x.replace(".", "").isdigit() and "." in x)
    #         .sum(),
    #         "integer": lambda df, col: df[col].apply(lambda x: x.isdigit()).sum(),
    #         "datetime": lambda df, col: pandas.to_datetime(
    #             df[col], errors="coerce", infer_datetime_format=True
    #         )
    #         .notna()
    #         .sum(),
    #         "bool": lambda df, col: df[col].apply(lambda x: x == "True" or x == "False").sum(),
    #     }

    #     # Iterate on each column of the dataframe and get the type with maximum number of values
    #     df_dtypes = {}
    #     for col in df.columns:
    #         results = {key: helper(df, col) for key, helper in helpers.items()}
    #         best_result = max(results, key=results.get)
    #         df_dtypes[col] = best_result if max(results.values()) else "string"
    #     self.types_guess = df_dtypes
