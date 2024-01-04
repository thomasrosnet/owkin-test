import logging
import unittest
import sys


from OwkinDataFrame import OwkinDataFrame


class ReadCSVTestCase(unittest.TestCase):
    filepath = "data/fake_dataset_(2).csv"

    def test_readcsv(self):
        print("test")
        data = OwkinDataFrame(self.filepath)
        print(data.get_types_columns())

        # attributes = [attr for attr in dir(data) if not attr.startswith('__')]
        # print(attributes)
        print(data.get_json_df())
        print(data.get_df_info())
        print(data.get_not_null())
        self.assertEqual(18, data.get_nb_columns())
        self.assertEqual(39, data.get_nb_row())

    # def test_radcsv_messytable(self):
    #     data = OwkinDataFrame(self.filepath)
    #     print(data.get_types_guess)

    #     self.assertEqual(38, data.get_nb_row())

    def test_validator(self):
        data = OwkinDataFrame(self.filepath)
        data.guess_types_col()

        self.assertEqual(39, data.get_nb_row())


if __name__ == "__main__":
    unittest.main()
