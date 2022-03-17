import os
import re
import shutil
import sqlite3
import pandas as pd


#-----------------------------------------------
# Make datasets folder
dataset_dir = 'datasets'

try:
    mkdir = 'mkdir {0}'.format(dataset_dir)
    os.system(mkdir)
    print("Folder created successfully")
except:
    print("Directory already exists or there is another error")


#-----------------------------------------------
# Change directory
os.chdir("csv")
print("Directory changed to csv folder")


#-----------------------------------------------
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


#-----------------------------------------------
# Make list of CSVs
csv_files = []

for file in os.listdir(os.getcwd()):
    if file.endswith('.csv'):
        csv_files.append(file)


#-----------------------------------------------
# Read CSVs 
data_path = '../'+dataset_dir+'/'

df = {}
for file in csv_files:
    try:
        df[file] = pd.read_csv(data_path+file)
        print(f"{file} read successfully")
    except UnicodeDecodeError:
        df[file] = pd.read_csv(data_path+file, encoding="ISO-8859-1")


#-----------------------------------------------
# Test df 
print(df['Company Client List.csv'].head())
print(df['Company Orders.csv'].head())


#-----------------------------------------------
# Change directory
os.chdir("..")
os.listdir(os.getcwd())


#-----------------------------------------------
# Make database folder
database_dir = 'database'

try:
    mkdir = 'mkdir {0}'.format(database_dir)
    os.system(mkdir)
    print("Folder created successfully")
except:
    print("Directory already exists or there is another error")


#-----------------------------------------------
# Change directory
os.listdir(os.getcwd())
os.chdir(database_dir)


#-----------------------------------------------
# ETL to db
for k in csv_files:    
    dataframe = df[k]
    
    # Clean table name
    clean_table_name = k.lower().replace(" ", "_").replace(r"/""\\", "_")
    clean_table_name = re.sub(r'[^a-zA-Z0-9_.]','', clean_table_name)    
    
    #Clean table data
    dataframe.columns = [x.lower().replace(" ", "_").replace(r"/""\\", "_").strip() for x in dataframe.columns]
    dataframe.columns = dataframe.columns.str.replace('[^A-Za-z\s_.]+', '', regex=True)
    
    table_name = '{0}'.format(clean_table_name.split('.')[0])
    
    # Change data types
    new_dtypes = {
    'object': 'varchar',
    'float64': 'float',
    'int64': 'int',
    'datetime64': 'timestamp',
    'timedelta64[ns]': 'varchar'
    }
    
    col_strings = ", ".join("{} {}".format(n, d) for (n, d) in zip(dataframe.columns, dataframe.dtypes.replace(new_dtypes)))
    
    # Write to db with SQLite
    conn = sqlite3.connect('company.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS table_name (
    col_strings    
    )
    ''')
    print('{0} was created successfully'.format(table_name))
    conn.commit()
    
    dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
    
    conn.close()