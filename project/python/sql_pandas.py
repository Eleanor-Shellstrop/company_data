import pandas as pd
from pathlib import Path
from query import all_clients, all_data


def df_all_fields(data):
    df_all = pd.DataFrame(
        data=data,
        columns=
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
        ]
    )
    return df_all


def df_client_orders(data):
    df_orders = pd.DataFrame(
        data=data, 
        columns=
        [
            'company_id',
            'company_name',
            'contact_first_name',
            'contact_last_name',
            'order_amount'
        ]
    )
    return df_orders


def csv_for_tableau(csv_name, var):
    filepath = Path('../tableau/'+ csv_name + '.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    var.to_csv(filepath)


def clean_order_amt():
    """Format and clean order_amount col"""
    df_orders = df_client_orders(all_clients)
    
    df_orders['order_amount'] = (
        df_orders['order_amount']
        .str.replace('$', '', regex=True)
        )
    df_orders = df_orders.astype({'order_amount': 'float'})
    df_orders.columns = [x.strip() for x in df_orders.columns]
    return df_orders


def order_vars():
    """Variables to use if needed"""
    df_orders = clean_order_amt()

    # DF totals of order by contacts
    contact_totals = (df_orders.groupby(
        ['company_name', 
        'contact_first_name', 
        'contact_last_name'
        ])
        .order_amount
        .sum()
        .reset_index())

    # Format money
    def money(new_var, old_var, text):
        new_var = "{:,}".format(old_var)
        print(f"{text}: ${new_var}")
        
    # USD total orders
    order_total = df_orders['order_amount'].sum()
    orders_formatted = money('orders_formatted', order_total, "All orders total")

    # USD order total with contacts
    contact_totals = (df_orders[df_orders['company_id'].notna()]['order_amount'].sum())
    contact_formatted = money('contact_formatted', contact_totals, "Orders with contacts total")

    # USD order total without contacts
    no_contact_totals = df_orders[df_orders['company_id'].isna()]['order_amount'].sum()
    no_contact_formatted = money('no_contact_formatted', no_contact_totals, "Orders without contacts total")
    
    return orders_formatted, contact_formatted, no_contact_formatted


def main():
    df_all_fields(all_data)
    df_all = df_all_fields(all_data)
    csv_for_tableau('all', df_all)

    df_client_orders(all_clients)
    orders = df_client_orders(all_clients)
    csv_for_tableau('orders', orders)

    order_vars()


if __name__ == '__main__':
    main()