import pandas
import pathlib
import configparser
from tabulate import tabulate
import logging

# set config path
config_path = pathlib.Path(__file__).parent.absolute() / "config.ini"
# creating the object of configparser
config = configparser.ConfigParser()
# reading data
config.read(config_path)


class OwkinDataFrame:

    dataframe = ""
    nb_row = ""
    nb_columns = ""
    header_list = ""
    types_columns = ""


    df_metadata = ""



    def __init__(self, csv):
        self.dataframe = self.readcsv(csv)
        self.nb_columns = len(self.dataframe.columns)
        self.nb_row = len(self.dataframe)
        self.types_columns = self.dataframe.dtypes

    def readcsv(self, csv):

        # data_folder = "../data/"
        print(csv)
        df = pandas.read_csv(csv, sep=";")
        # df = pandas.read_csv("data/fake_dataset_(2).csv", sep=";")

        # displaying the DataFrame
        # print(tabulate(df, headers = 'keys', tablefmt = 'psql'))

        print(len(df.columns))
        print(len(df))
        return df
    
    def get_nb_row(self):
        return self.nb_row

    def get_nb_columns(self):
        return self.nb_columns

    def get_types_columns(self):
        return self.types_columns.to_dict()
    
    def get_df_info(self):
        return self.dataframe.info()