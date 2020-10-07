import requests
from bs4 import BeautifulSoup
import pandas as pd
from lxml import html
from datetime import date
import numpy as np
import re
from Translations import euro_trans
import regions as r
import unicodedata
import regex

## Functions

#Function to "normalize" text when comparing the dictionnary data to scraped data from RKI (example: ç -> c)

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3 
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)     

def similar(str1, str2):
    return regex.search(rf'\b({str1}){{e<2}}\b',str2,flags=regex.IGNORECASE)

###





url = 'https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Risikogebiete_neu.html'

html = requests.get(url).content

soup = BeautifulSoup(html, "html.parser")

RKI_geb = soup.find("div", attrs={"class": "text"}).find_all("ul")

filtered = [i.get_text(strip=True) for i in RKI_geb]
    
countries = filtered[0].split(")")

Risikogebiete = [i for i in euro_trans.values() for st in countries if i in st]

if date.today().weekday() == 0:
    Risikogebiet_df = pd.DataFrame(euro_trans.items(), columns = ["country", "land"]).sort_values(by=['country']).reset_index(drop = True)
    Risikogebiet_df[f"{date.today()}"] = np.where(Risikogebiet_df["land"].isin(Risikogebiete), 1, 0)
    path = f"../Data/Risikogebiete_DE_week_{date.today()}.csv"
    Risikogebiet_df.to_csv(path)
else:
    week = date.today() - pd.to_timedelta((date.today().weekday()), unit='d')
    path = f"Data/Risikogebiete_DE_week_{week}.csv"
    Risikogebiet_df = pd.read_csv(path, index_col=0)
    Risikogebiet_df[f"{date.today()}"] = np.where(Risikogebiet_df["land"].isin(Risikogebiete), 1, 0)
    Risikogebiet_df.to_csv(path)



to_filter = soup.find("div", attrs={"class": "text"}).find("ul").find_all("li", recursive=False)

Region_lk = [i.get_text().replace("\n" , "").replace("–" , "") for i in to_filter if "<ul>" in str(i)]        

for i in euro_trans.values():
    for st in Region_lk:
        if i in st and not i == "Gibraltar": #Not .lower() or else irland would be found twice (Irland and Nordirland)
            path = f"{i}_regions"
            if "ausnahme" in st.lower() and not i == "Österreich":
                risk_regions = [r for r in r.regions[f"{i.lower()}"] if strip_accents(r.lower()) not in strip_accents(st.lower())]
                print(f'{i} : {risk_regions}')
            else:
                risk_regions = [r for r in r.regions[f"{i.lower()}"] if similar(strip_accents(r.lower()), strip_accents(st.lower()))]
                print(f'{i} : {risk_regions}')


       