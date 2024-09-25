import urllib
from io import BytesIO
from PyPDF2 import PdfReader
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = 'https://pubfiles.pagasa.dost.gov.ph/cds/'

def fetch_soup(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def dms_to_decimal(degrees, minutes, seconds):
    decimal_loc = float(degrees) + float(minutes) / 60 + float(seconds) / 3600
    return round(decimal_loc, 6)


def get_loc():
    soup = fetch_soup(URL)
    pdf_files = [a['href'] for a in soup.find_all('a') if a['href'].endswith('.pdf')]
    
    data = []
    
    for pdf in pdf_files:
        NEW_PATH = URL + pdf
        station_name = pdf[:-4].replace('_', ' ')
    
        wFile = urllib.request.urlopen(NEW_PATH)
        bytes_stream = BytesIO(wFile.read())
        
        reader = PdfReader(bytes_stream)
        
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            # Use regex to find latitude and longitude
            lat_pattern = re.compile(r"latitude.*?(\d+)o\s*(\d+)'\s*(\d+)\"?", re.IGNORECASE)
            lon_pattern = re.compile(r"longitude.*?(\d+)o\s*(\d+)'\s*(\d+)\"?", re.IGNORECASE)
    
            # Find matches for latitude and longitude
            lat_matches = lat_pattern.findall(text)
            # Find matches for longitude
            lon_matches = lon_pattern.findall(text)
    
            # If latitude and longitude matches found, store them in the data list
            if lat_matches and lon_matches:
                for lat_match, lon_match in zip(lat_matches, lon_matches):
                    lat_degrees, lat_minutes, lat_seconds = lat_match[0], lat_match[1], lat_match[2] if len(lat_match) > 2 else "00"
                    lon_degrees, lon_minutes, lon_seconds = lon_match[0], lon_match[1], lon_match[2] if len(lon_match) > 2 else "00"
                    
                    # Convert DMS to decimal
                    latitude_decimal = dms_to_decimal(lat_degrees, lat_minutes, lat_seconds)
                    longitude_decimal = dms_to_decimal(lon_degrees, lon_minutes, lon_seconds)
                    
                    data.append({
                        'station': station_name,
                        'latitude': latitude_decimal,
                        'longitude': longitude_decimal
                    })
    
        df = pd.DataFrame(data)
    
    return df
