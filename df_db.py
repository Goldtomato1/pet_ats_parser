from sqlalchemy import create_engine
import pandas as pd
import psycopg2


def df_to_pg(df):
    conn_string = 'postgresql://postgres:qawsed@127.0.0.1:5434/ats_parse'
    db = create_engine(conn_string)
    conn = db.connect()
    conn1 = psycopg2.connect(
        database="ats_parse",
        user='postgres',
        password='qawsed',
        host='127.0.0.1',
        port='5434'
    )
    conn1.autocommit = True
    cursor = conn1.cursor()
    cursor.execute('drop table if exists fact_region')
    sql = '''
        CREATE TABLE fact_region(
            date date,
            hour integer,
            val numeric(10,3));
    '''
    cursor.execute(sql)
    df.to_sql('fact_region', conn, index=False, if_exists='append')


def pg_to_df():
    conn_string = 'postgresql://postgres:qawsed@127.0.0.1:5434/ats_parse'
    db = create_engine(conn_string)
    conn = db.connect()
    return pd.read_sql_table('fact_region', conn)
