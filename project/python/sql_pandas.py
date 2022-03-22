import pandas as pd
from pathlib import Path
from query import all_clients, all_data


#-----------------------------------------------
# Create df: Combined tables
full = pd.DataFrame(data=all_data, columns=
                  [
                      'client_number',
                      'company_name',
                      'order_number',
                      'order_amount',
                      'order_date',
                      'paid',
                      'contact_first_name',
                      'contact_last_name',
                      'email',
                      'phone'
                  ])


#-----------------------------------------------
# Make csv for Tableau
filepath = Path('../tableau/all.csv')

filepath.parent.mkdir(parents=True, exist_ok=True)  

full.to_csv(filepath)  


#-----------------------------------------------
# Make df: Orders and contacts
df = pd.DataFrame(data=all_clients, columns=
                  [
                      'company_id',
                      'company_name',
                      'contact_first_name',
                      'contact_last_name',
                      'order_amount'
                  ])




#-----------------------------------------------
# Make CSV in new folder
filepath = Path('../tableau/orders.csv')

filepath.parent.mkdir(parents=True, exist_ok=True)  

df.to_csv(filepath)  


#-----------------------------------------------
# Change order dtpye
df['order_amount'] = df['order_amount'].str.replace('$', '', regex=True)

df = df.astype({'order_amount': 'float'})


#-----------------------------------------------
# Strip any whitespace

df.columns = [x.strip() for x in df.columns]


#-----------------------------------------------
# Store variables for use
# if needed

# DF totals of order by contacts
contact_totals = df.groupby(['company_name', 'contact_first_name', 'contact_last_name']).order_amount.sum().reset_index()

# Format money
def money(new_var, old_var, text):
    new_var = "{:,}".format(old_var)
    print(f"{text}: ${new_var}")
    
# USD total orders
order_total = df['order_amount'].sum()
money('orders_formatted', order_total, "All orders total")

# USD order total with contacts
contact_totals = df[df['company_id'].notna()]['order_amount'].sum()
money('contact_formatted', contact_totals, "Orders with contacts total")

# USD order total without contacts
no_contact_totals = df[df['company_id'].isna()]['order_amount'].sum()
money('no_contact_formatted', no_contact_totals, "Orders without contacts total")