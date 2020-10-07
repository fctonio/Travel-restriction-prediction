import importlib

importlib.import_module("model")
from model import estimate 

importlib.import_module("covid_cases_uk")
from covid_cases_uk import update_data_uk 

region = 'Liguria'
country = 'it'
path = f'Data/{country}/Covid_cases_{country}_7days_average.csv'

#update_data_uk()
print(estimate(path, region))