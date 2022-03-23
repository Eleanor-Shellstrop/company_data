import os
import sqlite3


#-----------------------------------------------
#Change directory
os.chdir('../database')


#-----------------------------------------------
# Missing Client Contacts
conn = sqlite3.connect('company.db')
c = conn.cursor()

c.execute('''
SELECT
    test_orders.company_name,
    contact_first_name,
    contact_last_name,
    order_amount
FROM
    test_orders
LEFT JOIN test_client_list ON test_client_list.company_name = test_orders.company_name
WHERE test_client_list.contact_last_name IS NULL;
''')

missing_contacts = []

for row in c.fetchall():
    missing_contacts.append(row)
    
conn.commit()
conn.close()


#-----------------------------------------------
# Left join to see missing contacts 
# in a full list
conn = sqlite3.connect('company.db')
c = conn.cursor()

c.execute('''
SELECT
    client_number,
    test_orders.company_name,
    contact_first_name,
    contact_last_name,
    order_amount
FROM
    test_orders
LEFT JOIN test_client_list ON test_client_list.company_name = test_orders.company_name;
''')

all_clients = []

for row in c.fetchall():
    all_clients.append(row)
    
conn.commit()
conn.close()


#-----------------------------------------------
# Left join and all rows 
# for a full list

conn = sqlite3.connect('company.db')
c = conn.cursor()

c.execute('''
SELECT
    client_number,
    test_orders.company_name,
    order_number,
    order_amount,
    order_date,
    paid,
    contact_first_name,
    contact_last_name,
    email,
    phone
FROM
    test_orders
LEFT JOIN test_client_list ON test_client_list.company_name = test_orders.company_name;
''')

all_data = []

for row in c.fetchall():
    all_data.append(row)
    
conn.commit()
conn.close()