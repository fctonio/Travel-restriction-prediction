import importlib
import streamlit as st
from datetime import date

importlib.import_module("model")
from model import estimate 

importlib.import_module("covid_cases_uk")
from covid_cases_uk import update_data_uk 

update_data_uk()

geocode_dict = {'Country':'', 'United Kingdom' : 'uk', 'Italy' : 'it', 'Switzerland' : 'ch'}

st.title("Your corona travel assistant")
st.markdown('Travelling made easy during difficult times')

country = st.selectbox(
    'Where would you like to go?',
    ('Country','United Kingdom', 'Italy', 'Switzerland'))

geocode = geocode_dict[country]

path = f'../Data/{geocode}/Covid_cases_{geocode}_7days_average.csv'

if geocode == 'uk': 
    st.image('https://i.pinimg.com/originals/0f/aa/4a/0faa4a9fbcc69d4fe73c3dc417367a85.jpg', width = 700)
    region = st.selectbox(
    'Select a region?',
    ('South East',
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
    'Wales'))
    data, fig = estimate(path, region)

if geocode == 'it': 
    st.image('https://i1.wp.com/www.travelrepublic.co.uk/blog//wp-content/uploads/2016/04/Italy-Map-2.jpg?ssl=1', width = 700)
    region = st.selectbox(
    'Select a region?',
    ('Abruzzo',
    'Basilicata',
    #'Calabria',
    'Campania',
    #'Emilia-Romagna',
    #'Friuli Venezia Giulia',
    #'Lazio',
    'Liguria',
    #'Lombardia',
    'Marche',
    'Molise',
    'P.A. Bolzano',
    'P.A. Trento',
    'Piemonte',
    #'Puglia',
    #'Sardegna',
    'Sicilia',
    'Toscana',
    'Umbria',
    'Valle d\'Aosta',
    'Veneto'))
    data, fig = estimate(path, region)

if geocode == 'ch': 
    st.image('https://upload.wikimedia.org/wikipedia/commons/4/4a/Switzerland%2C_administrative_divisions_-_de_-_colored.svg', width = 700)
    region = st.selectbox(
    'Select a region?',
    ('Zürich',
     'Bern',
     'Luzern',
     'Uri',
     'Schwyz',
     'Obwalden',
     'Nidwalden',
     'Glarus',
     'Zug',
     'Fribourg',
     'Solothurn',
     'Basel-Stadt',
     'Basel-Landschaft',
     'Schaffhausen',
     'Appenzell Ausserrhoden',
     'Appenzell Innerrhoden',
     'St.Gallen',
     'Graubünden',
     'Aargau',
     'Thurgau',
     'Ticino',
     'Vaud',
     'Valais',
     'Neuchâtel',
     'Genève',
     'Jura'))
    data, fig = estimate(path, region)

if geocode == '':
    st.image('https://1.bp.blogspot.com/-juBdhphcEwo/X33FLauzQqI/AAAAAAACeCY/kv9SB73QvpABg20xXHg4G9xdwCBUvLKeQCLcBGAsYHQ/s2048/Lets%2BWear%2BA%2BMask%2B01.jpg', width = 700)

if geocode in ['uk', 'ch', 'it']:
    if estimate(path, region):
        if data != None:
            data = str(data)
            if data > date.today().strftime("%Y-%m-%d"):
                st.markdown('We estimate that on the following date the critical threshold of 50 per 100 000 over 7 days will be broken:')
                st.warning(data)
            if data <= date.today().strftime("%Y-%m-%d"):
                st.markdown('Even if this region is maybe not a Risikogebiet just yet, it has already broken the critical threshold of 50 per 100 000 over 7 days on the:')
                st.error(data)
            st.write(fig)
        else:
            st.markdown('For the next 20 days we think it is...')
            st.success('Safe to travel!')
            st.write(fig)
