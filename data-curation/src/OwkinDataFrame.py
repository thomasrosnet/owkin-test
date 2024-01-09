import pandas
import json
import pathlib
import configparser
from tabulate import tabulate
import logging
import time
from src.Validator import Validator
from src.ValidatorCol import ValidatorCol
from src.ValidatorRow import ValidatorRow


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
    curated_dataframe = ""
    # types_guess = ""
    json_dataframe = ""
    nb_rows = 0
    nb_columns = 0
    header_list = ""
    types_columns = ""
    nb_total = 0
    nb_valid = 0
    nb_invalid = 0
    nb_missing = 0
    rate_valid = 0
    rate_invalid = 0
    rate_missing = 0

    col_name_type = {}

    row_threshold = 0.1
    col_threshold = 0.1

    df_notnull = ""

    rows_quality = {}
    columns_quality = {}
    dataset_metadata = {}

    def __init__(self, csv, row_threshold=0.1):
        """
        _summary_

        Args:
            csv (_type_): CSV file with observations as row and columns as variables
            row_threshold (float, optional): Value range from 0 to 1 (0 Accept every values). Defaults to 0.1.
        """        
        self.dataframe = self.readcsv_panda(csv)
        self.row_threshold = row_threshold

        self.nb_columns = len(self.dataframe.columns)
        self.nb_rows = len(self.dataframe)
        self.types_columns = self.dataframe.dtypes
        self.json_dataframe = self.dataframe.transpose().to_json()

        self.df_notnull = self.dataframe.count().to_json()

        self.header_list = self.dataframe.columns.values.tolist()
        self.nb_missing = int(self.dataframe.isna().sum().sum())
        self.nb_total = int(self.dataframe.count().sum()) + self.nb_missing

        # col summary + guess type
        self.guess_types_col()

        # row summary
        self.validate_rows()

        self.calculate_rates()

        # general summary
        self.dataset_metadata()
        # print(self.dataset_json_metadata)

        #test replacing incorrect values by NA
        # self.cure_dataframe()
        # print(self.curated_dataframe.dtypes)




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

    def dataset_metadata(self):
        dataset_metadata = {
            "nb_rows": self.nb_rows,
            "nb_rows_valid": self.nb_rows_valid,
            "nb_columns": self.nb_columns,
            "nb_total": self.nb_total,
            "nb_valid": self.nb_valid,
            "nb_invalid": self.nb_invalid,
            "nb_missing": self.nb_missing,
            "rate_valid": self.rate_valid,
            "rate_invalid": self.rate_invalid,
            "rate_missing": self.rate_missing,
            "headers_info": self.col_name_type,
            "columns_report": self.columns_quality,
            "row_treshold": self.row_threshold,
            "rows_report": self.rows_quality
        }
        self.dataset_metadata = dataset_metadata
        self.dataset_json_metadata = json.dumps(dataset_metadata)

    def guess_types_col(self):
        """
        Call ValidatorCol on each column to get a dict report of the column
        """        
        df = self.dataframe

        col_name_type = {}
        columns_quality = {}

        # nb_values_total =
        nb_valid = 0
        nb_invalid = 0

        # run column validation
        for col_name in self.header_list:
            column_validator = ValidatorCol(df[col_name])
            # print(column_info)
            col_name_type[col_name] = column_validator.get_guessed_type()

            columns_quality[col_name] = column_validator.get_column_quality()
            nb_valid += column_validator.get_nb_valid()
            nb_invalid += column_validator.get_nb_invalid()

        self.nb_valid = nb_valid
        self.nb_invalid = nb_invalid
        self.col_name_type = col_name_type
        self.columns_quality = columns_quality

    def validate_rows(self):
        """
        Call ValidatorRow on each row to get a dict report of the row
        """        
        
        rows_quality = {}
        nb_rows_valid = 0
        for index, df_row in self.dataframe.iterrows():
            row_validator = ValidatorRow(index, df_row, self.col_name_type, self.row_threshold)

            rows_quality[index] = row_validator.get_row_quality()
            if row_validator.get_is_row_valid():
                nb_rows_valid += 1
        
        self.nb_rows_valid = nb_rows_valid
        self.rows_quality = rows_quality
                
    def calculate_rates(self):
        self.rate_valid = round(self.nb_valid / self.nb_total, 4)
        self.rate_invalid = round(self.nb_invalid / self.nb_total, 4)
        self.rate_missing = round(self.nb_missing / self.nb_total, 4)

    def cure_dataframe(self):
        self.curated_dataframe = self.dataframe
        columns_report = self.dataset_metadata["columns_report"]
        for col_name in columns_report.keys():
            for index in columns_report[col_name]["invalid_values"].keys():
                # print(f"{int(index)} / {col_name}")
                self.curated_dataframe.loc[int(index), col_name] = pandas.NA
        self.curated_dataframe.convert_dtypes()
        self.curated_dataframe.to_csv('../curation-output/curated_data.csv', index=False)

    def get_panda_dataframe(self):
        return self.dataframe

    def get_col_name_type(self):
        return self.col_name_type

    def get_nb_rows(self):
        return self.nb_rows

    def get_nb_columns(self):
        return self.nb_columns

    def get_types_columns(self):
        return self.types_columns.to_dict()

    def get_df_info(self):
        return self.dataframe.info()

    def get_nb_missing(self):
        return self.nb_missing

    def get_json_df(self):
        return self.json_dataframe

    def get_not_null(self):
        return self.df_notnull
    
    def get_dataset_metadata(self):
        return self.dataset_metadata
