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
    return pd.read_sql_table('fact_region', conn, index_col='date')


def big_nodes_prices_to_pg(df):
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
    cursor.execute('drop table if exists big_nodes_prices_pub')
    sql = '''
        CREATE TABLE big_nodes_prices_pub(
            date date,
            hour INT,
            id_node INT,
            name_node VARCHAR(120),
            u_nom INT,
            u_fact numeric(10,3),
            name_subj VARCHAR(120),
            price numeric(10,3)
            );
    '''
    cursor.execute(sql)
    df.to_sql('big_nodes_prices_pub', conn, index=False, if_exists='append')


def sell_units_to_pg(df):
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
    cursor.execute('drop table if exists sell_units')
    sql = '''
        CREATE TABLE sell_units(
            date date,
            hour INT,
            id_gen INT,
            name_gen VARCHAR(120),
            id_node INT,
            name_node VARCHAR(120),
            tech_min numeric(10,3),
            technol_min numeric(10,3),
            down_limit numeric(10,3),
            plan_vol numeric(10,3),
            up_limit numeric(10,3),
            tech_max numeric(10,3),
            technol_max numeric(10,3)
            );
    '''
    cursor.execute(sql)
    df.to_sql('sell_units', conn, index=False, if_exists='append')
