import requests
import pandas as pd
import numpy as np
import json
from datetime import date, timedelta
from pathlib import Path

#____________ Functions _____________#

def area(i):
    if i < 9:
        return 'region'
    else:
        return 'nation'

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def filecreator(start_date):
    path = f"Data/uk/Covid_cases_uk_total.csv"
    my_file = Path(path)
    if my_file.is_file():
        return 
    else:
        df = pd.DataFrame(index=regions)
        df['population'] = pop_list
        for d in daterange(start_date, date.today()+timedelta(days=1)):
            df[d] = 0
        df.to_csv(path)
#____________________________________#

#______________ Lists _______________#

regions = [ 'South East',
            'London',
            'North West',
            'East of England',
            'West Midlands',
            'South West',
            'Yorkshire and the Humber',
            'East Midlands',
            'North East',
            'Scotland',
            'Northern Ireland',
            'Wales']

pop_list = [9180135, #South East
            8961989, #London
            7341196, #North West
            6236072, #East of England
            5934037, #West Midlands
            5624696, #South West
            5502967, #Yorkshire and the Humber
            4835928, #East Midlands
            2669941, #North East'
            5463300, #Scotland
            1893667, #Northern Ireland
            3152879  #Wales
            ]     
#____________________________________#


def update_data_uk():
    start_date = date(2020, 8, 1)

    filecreator(start_date)

    uk_df = pd.read_csv(f'Data/uk/Covid_cases_uk_total.csv', index_col=0)

    for i in range(len(regions)):

        areaName = regions[i]

        url = f'https://api.coronavirus.data.gov.uk/v1/data?filters=areaType={area(i)};areaName={areaName}&structure={{"date":"date","Cases":"cumCasesBySpecimenDate"}}'

        response = requests.get(url).json()
        
        cl_dict = {x['date']:x['Cases'] for x in response['data']}

        for d in daterange(start_date, date.today()+timedelta(days=1)):
            if str(d) in cl_dict:
                uk_df.at[areaName,str(d)] = cl_dict[str(d)]
            else:
                uk_df.at[areaName,str(d)] = None
        
    uk_df.to_csv(f'Data/uk/Covid_cases_uk_total.csv')
        
    ## Calculate cases per 100 000 in a 7 day periode

    df_uk_seven = pd.DataFrame(index=regions)

    for d in daterange(start_date, date.today()+timedelta(days=1)):
        if (d+timedelta(days=7)) < date.today()+timedelta(days=1):
            df_uk_seven[str(d+timedelta(days=7))] = ((uk_df[str(d+timedelta(days=7))] - uk_df[str(d)]) * 100000)/uk_df['population']
            df_uk_seven = df_uk_seven.round(2)
            num = df_uk_seven._get_numeric_data()
            num[num < 0] = None

    df_uk_seven.to_csv(f'Data/uk/Covid_cases_uk_7days_average.csv')

update_data_uk()