import unittest
import pandas as pd
from pandas.testing import assert_frame_equal


class DFTests(unittest.TestCase):
	
	def setUp(self):
		try:
			df1 = pd.read_csv('../csv/test_client_list.csv')
			print("df1 read")
			df2 = pd.read_csv('../csv/test_orders.csv')
			print("df2 read")
		except IOError:
			print('Cannot open file')
		self.fixture = df1, df2

	def test_frame(self):
		try:
			df1 = pd.read_csv('../csv/test_client_list.csv')
			df2 = pd.read_csv('../csv/test_orders.csv')
			assert_frame_equal(df1, df2, check_dtype=False)
		except AssertionError:
			print("These dataframes are different and should not match to pass test.")
		self.fixture = df1, df2
	
	def entry_test(self):
		try:
			df = pd.read_csv('../csv/test_orders.csv')
			print("these lines should match:")
			print(df.iloc[[10]])
			print("10,Twinder,534980,$1014896.00,12/9/2020,true")
		except:
			print("Error")	


if __name__ == '__main__':
    unittest.main()