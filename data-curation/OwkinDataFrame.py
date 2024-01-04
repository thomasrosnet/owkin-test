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
    nb_row = ""
    nb_columns = ""
    header_list = ""
    types_columns = ""
    missing_values = ""

    df_notnull = ""

    df_metadata = ""

    def __init__(self, csv):
        self.dataframe = self.readcsv_panda(csv)

        self.nb_columns = len(self.dataframe.columns)
        self.nb_row = len(self.dataframe)
        self.types_columns = self.dataframe.dtypes
        self.json_dataframe = self.dataframe.transpose().to_json()

        self.df_notnull = self.dataframe.count().to_json()

        self.header_list = self.dataframe.columns.values.tolist()
        # self.missing_values = self.dataframe.isnull.sum()

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

    def guess_types_col(self):
        df = self.dataframe

        for col_name in self.header_list:
            column_info = Validator(df[col_name])
            print(column_info)

    def get_panda_dataframe(self):
        return self.dataframe

    # def get_types_guess(self):
    #     return self.types_guess

    def get_nb_row(self):
        return self.nb_row

    def get_nb_columns(self):
        return self.nb_columns

    def get_types_columns(self):
        return self.types_columns.to_dict()

    def get_df_info(self):
        return self.dataframe.info()

    def get_df_missing(self):
        return self.missing_values

    def get_json_df(self):
        return self.json_dataframe

    def get_not_null(self):
        return self.df_notnull
