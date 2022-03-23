import os
import re
import shutil
import sqlite3
import pandas as pd
import unittest


### Global Variables ###
csv_files = []
df = {}

### Global Functions ###
def test_money(new_var, old_var, text):
	new_var = "{:,}".format(old_var)
	print(f"{text}: ${new_var}")

def test_clean_tb_name(table):
	"""Clean table name"""
	clean_tb_name = (
		table.lower()
		.replace(" ", "_")
		.replace(r"/""\\", "_")
	)
	clean_tb_name = re.sub(
		r'[^a-zA-Z0-9_.]','', clean_tb_name
	)
	return clean_tb_name  

def test_clean_tb_cols(table, frame):
	"""Clean all entries in df"""
	clean_table_name = test_clean_tb_name(table) 
	frame.columns = [
		table.lower()
		.replace(" ", "_")
		.replace(r"/""\\", "_")
		.strip() 
		for table in frame.columns
	]
	frame.columns = (
		frame.columns
		.str.replace('[^A-Za-z\s_.]+', '', regex=True)
	)
	tbl_name = '{0}'.format(
		clean_table_name.split('.')[0]
	)
	# Change data types
	new_dtypes = {
		'object': 'varchar',
		'float64': 'float',
		'int64': 'int',
		'datetime64': 'timestamp',
		'timedelta64[ns]': 'varchar'
	}
	col_strings = (
		", ".join(
			f"{n} {d}"
			for (n, d) in zip(
				frame.columns,
				frame.dtypes.replace(new_dtypes)
			)
		)
	)
	return tbl_name, col_strings

def test_make_new_dir(dir_name):
		"""Add new directory"""
		try:
			mkdir = 'mkdir {0}'.format(dir_name)
			os.system(mkdir)
		except:
			print(
				f"Directory '{dir_name}' already exists or there is another error"
			)


### Unit Test Class ###

class PyTests(unittest.TestCase):
				
	def setUp(self):
		pass
	
	def test_a_make_dataset_dir(self):
		"""Make datasets folder and copy CSVs"""
		dataset_dir = 'datasets'
		os.chdir("../")
		test_make_new_dir(dataset_dir)
		os.chdir("csv")
		# Copy CSVs into datasets folder
		src_dir = "."
		dst_dir = "../datasets"
		try:
			for root, dirs, files in os.walk(src_dir):
				for f in files:
					if f.endswith('.csv'):
						shutil.copy(os.path.join(root,f), dst_dir)
						print(f"File '{f}' copied successfully")
		except:
			print("There are no CSV files to copy")

	def test_b_make_dataframe(self):
		"""Make dataframes from pandas"""
		os.chdir('../csv')
		for file in os.listdir(os.getcwd()):
			if file.endswith('.csv'):
				csv_files.append(file)
		# Read CSVs 
		data_path = '../datasets/'
		for file in csv_files:
			try:
				df[file] = pd.read_csv(data_path+file)
			except UnicodeDecodeError:
				df[file] = pd.read_csv(data_path+file, encoding="ISO-8859-1")

	def test_c_make_db_dir(self):
		"""Make a database directory"""
		os.chdir("..")
		database_dir = 'database'
		test_make_new_dir(database_dir)
		# To start make_db() in correct folder
		os.chdir(database_dir)
		
	def test_d_make_db(self):
		"""Turn each file into a table, make db"""
		for k in csv_files:    
			dataframe = df[k]
			table_name = test_clean_tb_cols(k, dataframe)[0]
			column_strings = test_clean_tb_cols(k, dataframe)[1]
			db_name = 'company.db'
			# Write to db with SQLite
			conn = sqlite3.connect(db_name)
			c = conn.cursor()
			c.execute(f'''
			CREATE TABLE IF NOT EXISTS {table_name} (
			{column_strings}    
			)
			''')
			print(
				f"Table '{table_name}' in database '{db_name}' was created successfully"
			)
			conn.commit()
			dataframe.to_sql(
				table_name, 
				conn, 
				if_exists='replace', 
				index=False
			)
			conn.close()

	def test_e_variables(self):
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