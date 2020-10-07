import pandas as pd
import requests
import io
import os
from datetime import date, timedelta

#____________ Functions _____________#

def population():
    url = 'https://it.wikipedia.org/wiki/Regione_(Italia)'
    df = pd.read_html(url , thousands='\xa0')[13]
    df_trans = df[['Regione', 'Popolazione (ab.)']].drop(df.tail(1).index)
    df_trans['Regione'] =df_trans['Regione'].str.replace('\xa0', '').astype(str)
    df_trans = df_trans.sort_values(by=['Regione'])
    pop_list = df_trans['Popolazione (ab.)'].tolist()
    pop_list.pop(15)
    pop_list.insert(11, 531178) ### Wikipedia gives us number of the Region Trentino-Alto Adige only
    pop_list.insert(12, 541098)
    return 

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
#____________________________________#

#______________ Dict _______________#


#___________________________________#

# start_date = date(2020, 8, 1)
# end_date = date.today() - timedelta(days=1)
# daterange = pd.date_range(start_date, end_date)
# it = pd.DataFrame()

# for single_date in daterange:
#     date = single_date.strftime("%Y-%m-%d")
#     url = f'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni-{date.replace("-","")}.csv'
#     df = pd.read_csv(url, index_col=0)
#     it = it.append(df)

# it = it[['data','denominazione_regione', 'totale_casi']]

# it['date'] = it['data']

# it['date']= pd.to_datetime(it['date']).dt.strftime("%Y-%m-%d")

# itt = pd.pivot_table(it ,index=["denominazione_regione"], columns = ['date'])

# itt.columns = itt.columns.droplevel()

it = pd.read_csv('Data/it/Covid_cases_it_total.csv', index_col=['denominazione_regione'])

it['2020-10-08'] = None

print(it)

df_it_seven = pd.DataFrame(index=it.index)

for d in daterange(date(2020, 8, 1), date.today()+timedelta(days=1)):
    if (d+timedelta(days=7)) < date.today()+timedelta(days=1):
        df_it_seven[str(d+timedelta(days=7))] = ((it[str(d+timedelta(days=7))] - it[str(d)]) * 100000)/it['population']
        df_it_seven = df_it_seven.round(2)
        num = df_it_seven._get_numeric_data()
        num[num < 0] = None

df_it_seven.to_csv(f'Data/it/Covid_cases_it_7days_average.csv')
