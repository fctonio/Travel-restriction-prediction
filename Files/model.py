import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import statsmodels.api as sm
from datetime import date, timedelta


#____________ Functions _____________#

def prepare_df(path):
    df_model = pd.read_csv(path, index_col=0)
    df_model = df_model.T
    cols = df_model.columns
    df_model[cols] = df_model[cols].apply(pd.to_numeric, errors='coerce')
    df_model = df_model.assign(t=range(1, len(df_model) + 1)) #adding time variable
    df_model = df_model.assign(const=1)
    df_model['t2'] = df_model['t'] * df_model['t']
    return df_model



#____________________________________#

def estimate(path, region):

    df= prepare_df(path)

    index = pd.date_range(df.index[-1], periods=20, freq='D')
    df_pred = pd.DataFrame(index=index, columns= df.columns)
    df_pred[df_pred.columns] = df_pred[df_pred.columns].apply(pd.to_numeric, errors='coerce')
    df_pred.index = df_pred.index.date
    lastt = int(df.t[-1])
    df_pred = df_pred.assign(t= range(lastt, len(df_pred) + lastt)) #adding time variable
    df_pred = df_pred.assign(const=1)
    df_pred['t2'] = df_pred['t'] * df_pred['t']

    con_df_pred = pd.concat([df, df_pred])

    con_df_pred.index = pd.to_datetime(con_df_pred.index).strftime("%Y-%m-%d")
    X = con_df_pred[["const", "t" ,"t2"]]
    y = con_df_pred[region] + 0.1 * np.random.normal(size= len(con_df_pred[region]))
    lr = sm.OLS(y, X, missing='drop').fit()
    con_df_pred[f'pre_{region}'] = lr.predict(X)

    pre_region = f'pre_{region}'

    fig, ax = plt.subplots(figsize=(10,6))

    ax.plot(con_df_pred['t'],
            con_df_pred[f'pre_{region}'],
            color="blue")

    ax.plot(con_df_pred['t'],
            con_df_pred[region],
            color="red")

    date = None

    if con_df_pred[region].max() > 50:
        date = con_df_pred[con_df_pred[region].gt(50)].index[0]
    if con_df_pred[f'pre_{region}'].max() > 50:
        date = con_df_pred[con_df_pred[pre_region].gt(50)].index[0]
    return date, fig

    # if con_df_pred[region].max() > 50:
    #     return f'{region} has already passed the critical threshold of 50 new cases per 100 000 people over the last 7 days on the {con_df_pred[con_df_pred[region].gt(50)].index[0]}'    
    # if con_df_pred[f'pre_{region}'].max() > 50:
    #     return f'We estimate that the critical threshold in {region} of 50 new cases per 100 000 people over the last 7 days will be passed on the {con_df_pred[con_df_pred[pre_region].gt(50)].index[0]}. We advise you to be back in Germany several days before that date.'
    # else:
    #     return f'We don\'t think {region} will be a Risikogebiet in the next 20 days.'

