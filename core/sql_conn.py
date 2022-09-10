# Objective: establish a direct connection the NK database and execute a query to pull exclusion determination history for selected users.

# Import libraries
import psycopg2
from psycopg2 import Error
import pandas as pd
from core.patient import Patient

def run_query(query,  params=tuple()):
    try:
        with psycopg2.connect(host='',
                              port='5432',
                              dbname='',
                              user='kcowie') as con:
            return pd.read_sql_query(query, con, params=params)
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
