from ats_parser import df_from_ats
from df_db import df_to_pg, pg_to_df
from matplotlib import pyplot as plt



def plotly_creator(func):
    def wrapper(*args, **kwargs):
        fig = func(*args, **kwargs).plot()
        return plt.show()
    return wrapper

@plotly_creator
def max_values(df):
    return df.resample('D').max().dropna().drop('hour', axis=1)



@plotly_creator
def min_values(df):
    return df.resample('D').min().dropna().drop('hour', axis=1)

def main():
    df = df_from_ats()
    df_to_pg(df)
    df_from_db = pg_to_df()
    max_day = max_values(df_from_db)
    min_day = min_values(df_from_db)


if __name__ == '__main__':
    main()

