#!/usr/bin/env python
# coding: utf-8

#Import libraries
import pandas as pd
import argparse
from sqlalchemy import create_engine
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name ='output.csv'

    os.system(f"wget {url} -O {csv_name}") 

    # Create the engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Create batches
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)
    #Read the data
    dfmain = pd.read_csv(csv_name, nrows=100)

    # Some preprocessing
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # Some preprocessing
    dfmain.tpep_pickup_datetime = pd.to_datetime(dfmain.tpep_pickup_datetime)
    dfmain.tpep_dropoff_datetime = pd.to_datetime(dfmain.tpep_dropoff_datetime)

    #Populate the database in batches
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        df = next(df_iter)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists='append')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingest CSV data to postgres')
    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='user name for postgres')
    parser.add_argument('--url', help='url of the csv')

    args = parser.parse_args()

    main(args)







