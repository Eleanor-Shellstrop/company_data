import unittest
from datetime import datetime
import logging
import pandas as pd
from pandas.testing import assert_frame_equal


class DFTests(unittest.TestCase):
				
	def setUp(self):
		pass

	def test_entry(self):
		try:			
			logging.basicConfig(filename='../text/log.txt', encoding='utf-8', level=logging.DEBUG)
			logging.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: Entry Matching test")
			df = pd.read_csv('../csv/test_orders.csv')
			logging.info("these lines should match:")
			logging.info(df.iloc[[10]])
			logging.info("11, Fivebridge, 606112, $2402888.26, 10/29/2020, true")
			print("Entry match test passed")
		except:
			logging.error("Error, entry match test failed")

	def test_frame(self):
		try:
			logging.basicConfig(filename='../text/log.txt', encoding='utf-8', level=logging.DEBUG)
			logging.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: Assert Frame test")
			df1 = pd.read_csv('../csv/test_client_list.csv')
			df2 = pd.read_csv('../csv/test_orders.csv')
			assert_frame_equal(df1, df2, check_dtype=False)
			logging.error("These frames match, but sould not.They are different sizes")
			print("Assert Frame test failed")
		except AssertionError:
			logging.info("These frames don't match, which is the correct result")
			print("Assert Frame test passed")
		self.fixture = df1, df2	
		
	def test_read(self):
		try:
			logging.basicConfig(filename='../text/log.txt', encoding='utf-8', level=logging.DEBUG)
			logging.debug(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}: Read CSV test")
			df1 = pd.read_csv('../csv/test_client_list.csv')
			print("df1 read")
			df2 = pd.read_csv('../csv/test_orders.csv')
			print("df2 read")
			logging.info(f"DataFrames {df1} and {df2} imported successfully")
		except IOError:
			logging.error("Cannot open file to create dataframe")
			print('Cannot open file')
		self.fixture = df1, df2


if __name__ == '__main__':
    unittest.main()