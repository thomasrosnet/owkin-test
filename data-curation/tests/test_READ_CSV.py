import logging
import unittest
import sys


from OwkinDataFrame import OwkinDataFrame

class ReadCSVTestCase(unittest.TestCase):
    def test_readcsv(self):
        print("teste")
        data = OwkinDataFrame("data/fake_dataset_(2).csv")
        print(data.get_types_columns())
        self.assertEqual(18, data.get_nb_columns());
        self.assertEqual(38, data.get_nb_row())

        

if __name__ == '__main__':
    unittest.main()
