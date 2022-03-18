import unittest
import pandas as pd


def test_money(new_var, old_var, text):
	new_var = "{:,}".format(old_var)
	print(f"{text}: ${new_var}")


class PyTests(unittest.TestCase):
				
	def setUp(self):
		pass
	
	def test_variables(self):
		# Read csv and change dtype
		df = pd.read_csv('../csv/test_orders.csv')
		df['Order amount'] = df['Order amount'].str.replace('$', '', regex=True)
		df = df.astype({'Order amount': 'float'})

		# USD total orders
		order_total = df['Order amount'].sum()
		print(f"Originial variable sum equals {order_total}")
		print("Function to format:")
		print(test_money('orders_formatted', order_total, "All orders total"))


if __name__ == '__main__':
    unittest.main()