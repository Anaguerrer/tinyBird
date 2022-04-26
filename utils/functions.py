import pandas as pd
import numpy as np
import logging

def generate_random_data(size, missing_weight, waiting_weight, returned_weight):
    try:
        logging.info('Creating dataframe')
        n = size
        missing_n = round(n*missing_weight)
        waiting_n = round(n*waiting_weight)
        returned_n= round(n*returned_weight)

        np.random.seed(0)
        col = ['tracking_order', 'shipped_date', 'waiting', 'waiting_date', 'delivered', 'delivered_date', 'returned', 'returned_date', 'missing', 'missing_date']
        # empty dataframe with selected columns
        df = pd.DataFrame(columns=col)
    
        # id generation for each order item
        order_code = list(range(n))
        df['tracking_order'] = order_code

        # random dates for shipping between 2 months
        date_range_for_shipping, dates_array_shipped = get_dates('1/3/2022', '30/4/2022', n)
        df['shipped_date'] = dates_array_shipped

        # assingment of the status based on the weights defined
        df.loc[df.tracking_order<=missing_n,'missing']=1
        df.loc[(df.tracking_order>missing_n) & (df.tracking_order<=waiting_n + missing_n),'waiting']=1
        df.loc[(df.tracking_order>waiting_n + missing_n) & (df.tracking_order<=waiting_n + missing_n  + returned_n),'returned']=1
        df.loc[df.tracking_order>waiting_n + missing_n,'delivered']=1
        

        # definition of dates for each status and order
        rg = [1,2,3,4]
        for date in date_range_for_shipping:
            df.loc[(df.shipped_date==date) & (df.missing==1),'missing_date']=date + pd.Timedelta(days=int(np.random.choice(rg, 1)))
            df.loc[(df.shipped_date==date) & (df.waiting==1),'waiting_date']=date + pd.Timedelta(days=int(np.random.choice(rg, 1)))
            df.loc[(df.shipped_date==date) & (df.delivered==1),'delivered_date']=date + pd.Timedelta(days=int(np.random.choice(rg, 1)))
            df.loc[(df.shipped_date==date) & (df.returned==1),'returned_date']=date + pd.Timedelta(days=int(np.random.choice(rg, 1)) + int(np.random.choice(rg, 1)))

        # set the rest of the values to 0
        df = df.fillna(0)
        return df
    except:
        logging.info('something went worng')


# function to obtain randon date array for possibles shipping
def get_dates(start, end, n):
    try:
        logging.info('Generating random dates')
        date_range = np.array(pd.date_range(start=start, end=end,freq='D'))
        dates_array_shipped = np.random.choice(date_range, n)

        return date_range, dates_array_shipped
    except:
        logging.info('error generating dates')


def insert_data_into_bigQuery(dataframe):
    print('inserting data in bigquery')


def get_chart_data(df):
    try:
        logging.info('Obtaining data for pie chart')
        returned = df.apply(lambda x: x['returned'] == 1, axis=1).sum()
        delivered = df.apply(lambda x: x['delivered'] == 1, axis=1).sum()
        missing = df.apply(lambda x: x['missing'] == 1, axis=1).sum()
        waiting = df.apply(lambda x: x['waiting'] == 1, axis=1).sum()
        return returned, delivered, missing, waiting
    except:
        logging.info('error obtaining data for pie chart')