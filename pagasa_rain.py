# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:42:22 2024

@author: JSR
"""

from bs4 import BeautifulSoup
import os
import pandas as pd
import requests
import pagasa_stations as loc
import re

output_path = os.path.dirname(os.path.abspath(__file__))

#Get HTML from response object
def fetch_soup(url):
    response = requests.get(url, verify=False)
    return BeautifulSoup(response.content, 'html.parser')

def get_table(response):
    soup = fetch_soup(response)
    table = soup.find('tbody')
    return table

def get_headers(response):
    soup = fetch_soup(response)
    table = soup.find('table')
    headers = [th.text.strip() for th in table.find('thead').find_all('th')]
    return headers

def read_tbl(table, headers):
    
    rows = []
    for tr in table.find_all('tr'):
        row_val = []
        for td in tr.find_all('td'):
            tmp = ""
            for cell in td.stripped_strings:
                tmp += cell
            if not tmp:
                print("No value")
            else:
                row_val.append(tmp)

        if(len(row_val) ==0):
            continue
        else:
            rows.append(row_val)

    df = pd.DataFrame(data=rows, columns=headers)
    df.columns = ['site_id', 'site_name', 'hourly_rain', 'elevation', 'ts_updated']
    df['ts_updated'] = pd.to_datetime(df['ts_updated'], format='%B %d, %Y, %I:%M %p')

    return df

def write_loc(data):
    location = loc.get_loc()
    
    remove = ['AWS', 'ARG']
    for word in remove:
        data['aws'] = data['site_name'].str.replace(word, '', regex=False)
    
    data['aws'] = data['aws'].str.split(',').str[0]
    data['aws'] = data['aws'].apply(lambda text: re.split(r'[-,]', text)[0] if text else None)
    data = pd.merge(data, location, left_on='aws', right_on='station', how='left')
    
    data = data.drop(columns=['aws', 'station'])
    
    return data

def main():
    URL = 'https://bagong.pagasa.dost.gov.ph/automated-rain-gauge'
    rain_table = get_table(URL)
    rain_headers = get_headers(URL)
    
    rain_data = read_tbl(rain_table, rain_headers)
    rain_data = write_loc(rain_data)
    rain_data.to_csv(os.path.join(output_path, 'pagasa_rain.csv'))
    
    print(rain_data)
    
if __name__ == "__main__":
    
    main()
