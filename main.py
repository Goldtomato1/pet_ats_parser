from ats_parser import df_from_ats
from df_db import df_to_pg, pg_to_df
import pandas as pd

pd.options.plotting.backend = "plotly"


def plotly_creator(func):
    def show(*args, **kwargs):
        df = func(*args, **kwargs)
        fig = df.plot()
        return fig.show()
    return show

@plotly_creator
def max_values(df):
    return df.resample('D').max().dropna().drop('hour', axis=1)
 #   return df[['date', 'val']].groupby('date').max('val')
@plotly_creator
def mean_values(df):
    return df.resample('D').mean().dropna().drop('hour', axis=1)

def main():
    #df = df_from_ats()
    #df_to_pg(df)
    df_from_db = pg_to_df()
    max_day = max_values(df_from_db)


if __name__ == '__main__':
    main()

