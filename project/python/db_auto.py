import os
import re
import shutil
import sqlite3
import pandas as pd


csv_files = []
df = {}

def make_new_dir(dir_name):
    try:
        mkdir = 'mkdir {0}'.format(dir_name)
        os.system(mkdir)
        print(f"Directory '{dir_name}' created successfully")
    except:
        print(f"Directory '{dir_name}' already exists or there is another error")


def make_dataset_dir():
    """Make datasets folder and copy CSVs"""
    dataset_dir = 'datasets'
    os.chdir("../")
    make_new_dir(dataset_dir)

    # Change directory
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



def make_df():
    """Make dataframes from pandas"""
    # Make list of CSVs
    for file in os.listdir(os.getcwd()):
        if file.endswith('.csv'):
            csv_files.append(file)

    # Read CSVs 
    data_path = '../datasets/'

    for file in csv_files:
        try:
            df[file] = pd.read_csv(data_path+file)
            print(f"{file} read successfully")
            print(f"df[{file}].head()")
        except UnicodeDecodeError:
            df[file] = pd.read_csv(data_path+file, encoding="ISO-8859-1")


def make_db_dir():
    """Make a database directory"""
    os.chdir("..")
    database_dir = 'database'
    make_new_dir(database_dir)
    # To start make_db() in correct folder
    os.chdir(database_dir)


# ETL to db
def make_db():
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

        c.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
        {col_strings}    
        )
        ''')
        print('{0} was created successfully'.format(table_name))
        conn.commit()
        
        dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
        
        conn.close()

def main():
    make_dataset_dir()
    make_df()
    make_db_dir()
    make_db()

if __name__ == '__main__':
    main()