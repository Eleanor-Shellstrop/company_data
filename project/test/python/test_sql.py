import unittest
from warnings import catch_warnings
from test_query import missing_contacts, all_clients, all_data


class SqlTests(unittest.TestCase):
				
	def setUp(self):
		pass

	def test_a_import_vars(self):
		try:
			missing = missing_contacts
			clients = all_clients
			data = all_data
			print(f"The first' missing contact' entry is {missing[0]}")
			print(f"The first 'client orders with contact' entry is {clients[0]}")
			print(f"The first 'all data' entry is {data[0]}")
		except:
			print("Variable import test failed")


if __name__ == '__main__':
    unittest.main()