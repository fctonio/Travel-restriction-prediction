import requests
import pandas as pd
import numpy as np
import json
from datetime import date

url = "https://covid-193.p.rapidapi.com/statistics"

headers = {
    'x-rapidapi-host': "covid-193.p.rapidapi.com",
    'x-rapidapi-key': "3ea1c14b00mshb6cedc9f4de354bp172633jsnc0ef76d6f7bd"
    }

result = requests.get(url, headers=headers)

pretty_json = json.loads(result.text)

all_df = pd.json_normalize(pretty_json['response'])

cases_df = all_df.copy().drop(['tests.1M_pop', 
             'deaths.1M_pop', 
             'deaths.new', 
             'cases.recovered',
             'cases.critical', 
             'cases.active', 
             'cases.1M_pop',
             'cases.new',
             'time'                 
            ],
            axis = 1
           )