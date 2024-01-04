import time
import pandas


class Validator:
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
    incorrect_miss = ""
    missing_count = ""
    incorrect_count = ""
    incorrect = ""
    score_summary = ""

    alpha_unique = []
    column_describe = {}

    def __init__(self, df_column):
        self.df_column = df_column
        self.df_column_name = df_column.name

        self.missing_count = self.df_column.apply(self.is_missing).sum()

        self.date_score = self.df_column.apply(self.validate_date).sum()
        self.int_score = self.df_column.apply(self.validate_int).sum()
        self.float_score = self.df_column.apply(self.validate_float).sum()
        self.alpha_score = self.df_column.apply(self.validate_alpha).sum()
        self.bool_score = self.df_column.apply(self.validate_bool).sum()

        self.score_summary()

        self.count_incorrect()
        self.select_incorrect()
        print(self.incorrect)

    def select_missing(self):
        pass

    def select_incorrect(self):
        match self.guessed_type:
            case "Date":
                self.incorrect = self.df_column[~self.df_column.apply(self.validate_date)].to_dict()
            case "Int":
                self.incorrect = self.df_column[~self.df_column.apply(self.validate_int)].to_dict()
            case "Float":
                self.incorrect = self.df_column[~self.df_column.apply(self.validate_float)].to_dict()
            case "Alpha":
                self.incorrect = self.df_column[~self.df_column.apply(self.validate_alpha)].to_dict()
            case "Boolean":
                self.incorrect = self.df_column[~self.df_column.apply(self.validate_bool)].to_dict()


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
            self.column_describe = self.df_column.describe().to_dict()

        if self.guessed_type == "Int":
            self.column_describe = self.df_column.describe().to_dict()

        if self.guessed_type == "Float":
            self.column_describe = self.df_column.describe().to_dict()

        # print(self.column_describe)

    def is_missing(self, value):
        return pandas.isna(value)
    
    def count_incorrect(self):
        self.incorrect_count = self.incorrect_miss - self.missing_count



    def validate_date(self, value):
        if pandas.isna(value):
            return False

        if type(value) is str:
            try:
                time.strptime(value, "%d/%m/%Y")
                return True
            except ValueError:
                return False
        return False

    def validate_int(self, value):
        if pandas.isna(value):
            return False

        if type(value) is int:
            return True
        if type(value) is str:
            return value.isdigit()
        return False

    def validate_float(self, value):
        if pandas.isna(value):
            return False

        if type(value) is float:
            return True
        if type(value) is str:
            return value.replace(".", "").isdigit() and "." in value
        return False

    def validate_alpha(self, value):
        if pandas.isna(value):
            return False

        if type(value) is str:
            value = value.replace(" ", "")
            if value.isalpha():
                return True
            if value.replace("+", "").isalpha():
                return True
        return False

    def validate_bool(self, value):
        if pandas.isna(value):
            return False

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
    
    def get_incorrect(self):
        return self.get_incorrect
    
    def to_json(self):
        pass

    def __str__(self):
        str = f"{self.df_column_name}:\t {self.guessed_type} | {self.max_score} | {self.incorrect_count} | {self.missing_count}"
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
