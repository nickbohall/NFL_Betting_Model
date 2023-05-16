import numpy as np
import pandas as pd

def dynamic_window_ewma(x):
    # Calculate rolling exponentially weighted EPA with a dynamic window size
    values = np.zeros(len(x))

    for i, (_, row) in enumerate(x.iterrows()):
        epa = x.epa_shifted[:i+1]
        if row.week > 10:
            values[i] = epa.ewm(min_periods=1, span=row.week).mean().values[-1]
        else:
            values[i] = epa.ewm(min_periods=1, span=10).mean().values[-1]

    return pd.Series(values, index=x.index)

def create_epa_df(data, epa_type, side):
    # Return a df based on the play data, epa type, and offense vs defense
    return data.loc[data[epa_type] == 1, :].groupby([side, 'season', 'week'], as_index=False)['epa'].mean()

def lag_df(df, side):
    return df.groupby(side)['epa'].shift()

def create_ewma(df, side):
    return df.groupby(side)['epa_shifted'].transform(lambda x: x.ewm(min_periods=1, span=10).mean())

def create_ewma_dynamic(df, side):
    return df.groupby(side).apply(dynamic_window_ewma).values
