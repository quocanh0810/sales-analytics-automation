import pandas as pd
import random

def clean_sales_data(df):
    # Gán TERRITORY theo COUNTRY
    df.loc[df['TERRITORY'].isna() & df['COUNTRY'].isin(['USA', 'Canada']), 'TERRITORY'] = 'NA'
    df.loc[df['TERRITORY'].isna() & df['COUNTRY'].isin(['Germany', 'France']), 'TERRITORY'] = 'EMEA'
    df.loc[df['TERRITORY'].isna() & df['COUNTRY'].isin(['Japan', 'China']), 'TERRITORY'] = 'APAC'
    df.loc[df['TERRITORY'].isna(), 'TERRITORY'] = 'LATAM'

    df['TERRITORY'] = df['TERRITORY'].fillna(random.choice(['NA', 'EMEA', 'APAC', 'LATAM']))

    return df