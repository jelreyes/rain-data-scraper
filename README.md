# PAGASA Data Scraper

## Overview

This repository contains two Python scripts designed to scrape and process data from the PAGASA (Philippine Atmospheric, Geophysical, and Astronomical Services Administration) website:

1. Rain Data Scraper: Scrapes automated rain gauge data from the PAGASA website and saves it to a CSV file.
2. PAGASA Stations Script: Extracts latitude and longitude information for various PAGASA stations from PDF files linked on the PAGASA site.

## Requirements

* Python 3.x
* requests: For making HTTP requests to fetch web content.
* BeautifulSoup: For parsing HTML content.
* pandas: For data manipulation and analysis.
* PyPDF2: For reading PDF files.

You can install the required packages using pip:

```bash
pip install requests beautifulsoup4 pandas PyPDF2
```

## Rain Data Scraper

## Functions

* fetch_soup(url): Fetches HTML content from the specified URL and returns a BeautifulSoup object.
* get_table(response): Extracts the <tbody> section from the HTML response.
* get_headers(response): Extracts the headers from the table in the HTML response.
* read_tbl(table, headers): Reads the table data and converts it into a pandas DataFrame.
* write_loc(data): Processes the DataFrame to associate each rain gauge with its location.
* main(): Orchestrates the workflow of scraping data, processing it, and saving it to a CSV file.

## Output
The output will be saved in a CSV file named pagasa_rain.csv, containing columns for site_id, site_name, hourly_rain, elevation, and ts_updated.

## PAGASA Stations Script

## Functions

* fetch_soup(url): Fetches HTML content from the specified URL and returns a BeautifulSoup object.
* dms_to_decimal(degrees, minutes, seconds): Converts DMS (Degrees, Minutes, Seconds) coordinates to decimal format.
* get_loc(): Scrapes the PAGASA website for PDF files, extracts latitude and longitude for each station, and returns a DataFrame with station names, latitudes, and longitudes.

## Output

The output will be a pandas DataFrame containing:

* station: Name of the PAGASA station.
* latitude
* longitude

## Notes

Ensure that the PAGASA website structure remains unchanged; otherwise, the scripts may require updates to adapt to any changes in the HTML structure or PDF formatting.
The scripts suppress SSL certificate verification (verify=False in requests.get) for simplicity, but it is advisable to enable SSL verification in production environments.

## Author

JSR 2024