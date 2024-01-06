import pandas
import numpy
import pathlib
import configparser
from tabulate import tabulate
import logging
import time
from Validator import Validator

# set config path
config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
# creating the object of configparser
config = configparser.ConfigParser()
# reading data
config.read(config_path)


class OwkinDataFrame:
    """
    _summary_

    Returns:
        _type_: _description_
    """

    dataframe = ""
    # types_guess = ""
    json_dataframe = ""
    nb_rows = ""
    nb_columns = ""
    header_list = ""
    types_columns = ""
    nb_missing_values = ""
    col_name_type = {}

    row_threshold = 0.1
    col_threshold = 0.1

    df_notnull = ""

    df_json_metadata = {}

    def __init__(self, csv):
        self.dataframe = self.readcsv_panda(csv)

        self.nb_columns = len(self.dataframe.columns)
        self.nb_rows = len(self.dataframe)
        self.types_columns = self.dataframe.dtypes
        self.json_dataframe = self.dataframe.transpose().to_json()

        self.df_notnull = self.dataframe.count().to_json()

        self.header_list = self.dataframe.columns.values.tolist()
        self.nb_missing_values = self.dataframe.isna().sum().sum()

        # general summary
        self.summary_to_json()

        # col summary + guess type
        self.guess_types_col()

        # row summary
        self.validate_rows(self.dataframe)


    def readcsv_panda(self, csv_path):
        # data_folder = "../data/"
        logging.debug(csv_path)
        df = pandas.read_csv(csv_path, sep=";")
        # df = pandas.read_csv("data/fake_dataset_(2).csv", sep=";")

        # displaying the DataFrame
        # print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

        logging.info(len(df.columns))
        logging.debug(len(df))
        logging.info(len(df))
        # print(len(df))

        return df

    def summary_to_json(self):
        self.df_json_metadata = {
            "nb_rows": self.nb_rows,
            "nb_columns": self.nb_columns,
            "nb_missing_values": self.nb_missing_values,
            "header_list": self.header_list,
            "columns_report": {},
            "rows_report": {}
        }

    def guess_types_col(self):
        df = self.dataframe

        col_name_type = {}

        for col_name in self.header_list:
            column_info = Validator(df[col_name])
            # print(column_info)
            col_name_type[col_name] = column_info.get_guessed_type()

        self.col_name_type = col_name_type

    def validate_rows(self, df):

        rows_quality = {}
        for index, row in df.iterrows():
            nb_valid = 0
            nb_invalid = 0
            invalid_values = {}
            for col_name in self.col_name_type.keys():
                
                # Call validate methods here
                match self.col_name_type[col_name]:
                    case "Date":
                        is_valid = Validator.validate_date(row[col_name])
                    case "Int":
                        is_valid = Validator.validate_int(row[col_name])
                    case "Float":
                        is_valid = Validator.validate_float(row[col_name])
                    case "Alpha":
                        is_valid = Validator.validate_alpha(row[col_name])
                    case "Boolean":
                        is_valid = Validator.validate_bool(row[col_name])
                if is_valid:
                    nb_valid += 1
                else:
                    nb_invalid += 1
                    invalid_values[col_name] = row[col_name]

            is_row_valid = bool(nb_invalid == 0)

            row_summary = {
                "nb_valid": nb_valid,
                "nb_invalid": nb_invalid,
                "is_row_valid": is_row_valid,
                "invalid_values": invalid_values
            }
            rows_quality[index] = row_summary
        
        print(rows_quality)
                


    def get_panda_dataframe(self):
        return self.dataframe

    # def get_types_guess(self):
    #     return self.types_guess

    def get_nb_rows(self):
        return self.nb_rows

    def get_nb_columns(self):
        return self.nb_columns

    def get_types_columns(self):
        return self.types_columns.to_dict()

    def get_df_info(self):
        return self.dataframe.info()

    def get_nb_missing(self):
        return self.nb_missing_values

    def get_json_df(self):
        return self.json_dataframe

    def get_not_null(self):
        return self.df_notnull
    
    def get_json_summary(self):
        return self.df_json_metadata
