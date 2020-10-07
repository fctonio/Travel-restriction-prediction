import pandas as pd
import requests
import io
import os
from datetime import date, timedelta

#____________ Functions _____________#

def population():
    url = 'https://de.wikipedia.org/wiki/Kanton_(Schweiz)'
    df = pd.read_html(url , thousands='\'')[0]
    df_trans = df[['Ein­wohner1', 'Kanton']].drop(df.tail(1).index)
    df_trans['Kanton'] =df_trans['Kanton'].str.replace('\xa0', '').astype(str)
    df_trans['kanueb'] = df_trans['Kanton'].map(ch_dict)
    df_trans = df_trans.sort_values(by=['kanueb'])
    return df_trans['Ein­wohner1'].tolist()

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
#____________________________________#

#______________ Dict _______________#

ch_dict = { 'Zürich': 'Zürich',
            'Bern': 'Bern',
            'Luzern': 'Luzern',
            'Uri': 'Uri',
            'Schwyz': 'Schwyz',
            'Obwalden': 'Obwalden',
            'Nidwalden': 'Nidwalden',
            'Glarus': 'Glarus',
            'Zug': 'Zug',
            'Freiburg': 'Fribourg',
            'Solothurn': 'Solothurn',
            'Basel-Stadt': 'Basel-Stadt',
            'Basel-Landschaft': 'Basel-Landschaft',
            'Schaffhausen': 'Schaffhausen',
            'AppenzellAusserrhoden': 'Appenzell Ausserrhoden',
            'AppenzellInnerrhoden': 'Appenzell Innerrhoden',
            'St.Gallen': 'St.Gallen',
            'Graubünden': 'Graubünden',
            'Aargau': 'Aargau',
            'Thurgau': 'Thurgau',
            'Tessin': 'Ticino',
            'Waadt': 'Vaud',
            'Wallis': 'Valais',
            'Neuenburg': 'Neuchâtel',
            'Genf': 'Genève',
            'Jura': 'Jura'
           }

#___________________________________#


url = 'https://data.bs.ch/explore/dataset/100077/download/?format=csv&timezone=Europe/Zurich&lang=de&use_labels_for_header=true&csv_separator=%3B'

s = requests.get(url).content

c = pd.read_csv(io.StringIO(s.decode('utf-8')), sep=';')

c = c[['Date', 'Canton', 'Cumulative number of confirmed cases']]

ct = pd.pivot_table(c ,index=["Canton"], columns = ['Date'])

ct.columns = ct.columns.droplevel()

ct = ct.loc[:, '2020-08-03':].fillna(method='ffill', axis = 1)

ct['population'] = population()

ct.to_csv('Data/ch/Covid_cases_ch_total.csv')

df_ch_seven = pd.DataFrame(index=ct.index)

for d in daterange(date(2020, 8, 3), date.today()+timedelta(days=1)):
    if (d+timedelta(days=7)) < date.today()+timedelta(days=1):
        df_ch_seven[str(d+timedelta(days=7))] = ((ct[str(d+timedelta(days=7))] - ct[str(d)]) * 100000)/ct['population']
        df_ch_seven = df_ch_seven.round(2)
        num = df_ch_seven._get_numeric_data()
        num[num < 0] = None

df_ch_seven.to_csv(f'Data/ch/Covid_cases_ch_7days_average.csv')
