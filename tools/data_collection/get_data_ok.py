"""
Get Cannabis Data for Oklahoma | Cannlytics

Author: Keegan Skeate
Contact: <keegan@cannlytics.com>
Created: 5/27/2021
Updated: 5/30/2021
License: MIT License <https://opensource.org/licenses/MIT>
Resources:
    - [Medical Marijuana Excise Tax](https://oklahomastate.opengov.com/transparency#/33894/accountType=revenues&embed=n&breakdown=types&currentYearAmount=cumulative&currentYearPeriod=months&graph=bar&legendSort=desc&month=5&proration=false&saved_view=105742&selection=A49C34CEBF1D01A1738CB89828C9274D&projections=null&projectionType=null&highlighting=null&highlightingVariance=null&year=2021&selectedDataSetIndex=null&fiscal_start=earliest&fiscal_end=latest)
    - [List of Licensed Businesses](https://oklahoma.gov/omma/businesses/list-of-businesses.html)
    - [SQ788](https://www.sos.ok.gov/documents/questions/788.pdf)
    - [How to Extract Text from a PDF](https://stackoverflow.com/questions/34837707/how-to-extract-text-from-a-pdf-file/63518022#63518022)
"""
import os
import fitz # pymupdf
import pandas as pd
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin

COLUMNS = [
    'name',
    'trade_name',
    'license_number',
    'email',
    'phone',
    'city',
    'zip_code',
    'county',
]

COUNTIES = [
    'Adair',
    'Alfalfa',
    'Atoka',
    'Beaver',
    'Beckham',
    'Blaine',
    'Bryan',
    'Caddo',
    'Canadian',
    'Carter',
    'Cherokee',
    'Choctaw',
    'Cimarron',
    'Cleveland',
    'Coal',
    'Comanche',
    'Cotton',
    'Craig',
    'Creek',
    'Custer',
    'Delaware',
    'Dewey',
    'Ellis',
    'Garfield',
    'Garvin',
    'Grady',
    'Grant',
    'Greer',
    'Harmon',
    'Harper',
    'Haskell',
    'Hughes',
    'Jackson',
    'Jefferson',
    'Johnston',
    'Kay',
    'Kingfisher',
    'Kiowa',
    'Latimer',
    'Le Flore',
    'Lincoln',
    'Logan',
    'Love',
    'Major',
    'Marshall',
    'Mayes',
    'McClain',
    'McCurtain',
    'McIntosh',
    'Murray',
    'Muskogee',
    'Noble',
    'Nowata',
    'Okfuskee',
    'Oklahoma',
    'Okmulgee',
    'Osage',
    'Ottawa',
    'Pawnee',
    'Payne',
    'Pittsburg',
    'Pontotoc',
    'Pottawatomie',
    'Pushmataha',
    'Roger Mills',
    'Rogers',
    'Seminole',
    'Sequoyah',
    'Stephens',
    'Texas',
    'Tillman',
    'Tulsa',
    'Wagoner',
    'Washington',
    'Washita',
    'Woods',
    'Woodward',
]
COUNTIES = [s.upper() for s in COUNTIES]

EXCLUDE = [
    '',
    'OMMA.ok.gov',
    'Page 518 of 518',
    'Oklahoma Medical Marijuana Authority',
    'Licensed Growers | May 26, 2021',
    'NAME',
    'ZIP',
    'PHONE',
    'CITY',
    'LICENSE No.',
    'EMAIL',
    'COUNTY',
]

EXLUDE_PARTS = [
    'Page ',
    'Licensed ',
    'LIST OF ',
    'As of '
]

LICENSEE_LISTS = [
    'https://oklahoma.gov/omma/businesses/list-of-businesses.html',
    'https://oklahoma.gov/omma/businesses/list-of-licensed-businesses/licensed-laboratories.html',
    'https://oklahoma.gov/omma/businesses/list-of-licensed-businesses/licensed-waste-disposal-facility.html',
]

MONTHS = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December' : 12,
}

TAX_RATE = 7


def download_website_pdfs(url, destination):
    """Download all PDFS from a given website to a given folder.
    Args:
        url (str): The website that contains the PDFs.
        destination (str): The destination for the PDFS.
    """
    files = []
    if not os.path.exists(destination): os.mkdir(destination)
    response = requests.get(url)
    soup= BeautifulSoup(response.text, 'html.parser')     
    for link in soup.select('a[href$=".pdf"]'):
        file_name = os.path.join(destination, link['href'].split('/')[-1])
        files.append(file_name)
        with open(file_name, 'wb') as f:
            f.write(requests.get(urljoin(url, link['href'])).content)
    return files


def parse_licensee_records(file_name):
    """Parse OMMA licensee records from a given licensee list.
    Args:
        url (str): The website that contains the PDFs.
        destination (str): The destination for the PDFS.
    """
    records = []
    with fitz.open(file_name) as doc:
        for page in doc:
            page_text = page.getText()
            values = page_text.replace(' \n \n', ' \n').split(' \n')
            row = []
            for value in values:
                if value in EXCLUDE or any(x in value for x in EXLUDE_PARTS):
                    continue
                row.append(value.title())
                if len(row) == 8:
                    records.append(row)
                    row = []
    return records


def clean_licensee_records(records):
    """Clean a list of lists of licensee records into a DataFrame.
    Args:
        records (list(list)): A list of a list of record values.
    """
    data = pd.DataFrame(records, columns=COLUMNS)
    data['trade_name'] = data['trade_name'].str.replace('Trade Name: ', '')
    data['email'] = data['email'].str.lower()
    data['license_number'] = data['license_number'].str.upper()
    return data


if __name__ == '__main__':

    # Dynamic data directory.
    try:
        directory = sys.argv[1]
    except IndexError:
        directory = r'C:\Users\keega\Documents\cannlytics\data\state_data\OK'

    # Download all licensee lists to a new folder in the directory.
    date = datetime.now().strftime('%Y-%m-%d')
    licensee_folder = os.path.join(directory, date)
    licensee_files = []
    for url in LICENSEE_LISTS:
        files = download_website_pdfs(url, licensee_folder)
        licensee_files += files
    
    # Parse and clean all licensee data.
    frames = []
    for file_name in licensee_files:
        license_type = file_name.split('omma_')[1].replace('_list.pdf', '')
        records = parse_licensee_records(file_name)
        data = clean_licensee_records(records)
        data['license_type'] = license_type
        frames.append(data)
    licensees = pd.concat(frames)
    
    # Save and upload data
    licensses.to_excel('')
    
    
    # Read Oklahoma tax data.
    # file_name = 'Oklahoma Data Snapshot - 5-29-2021'
    # ext = 'csv'
    # raw_excise_tax_data = pd.read_csv(
    #     f'{directory}/{file_name}.{ext}',
    #     skiprows=4
    # )
    
    # # Format excise tax.
    # excise_tax = []
    # raw_excise_tax = raw_excise_tax_data.iloc[1].to_dict()
    # for key, value in raw_excise_tax.items():
    #     if 'Actual' in key:
    #         timestring = key.replace(' Actual', '')
    #         parts = timestring.replace(' ', '-').split('-')
    #         month_name = parts[0]
    #         # FIXME: Format date dynamically
            
    #         # year = parts[1]
    #         # day = parts[2]
    #         month = MONTHS[month_name]
    #         if month < 6:
    #             year = '2021'
    #         else:
    #             year = '2020'
    #         excise_tax.append({
    #             'date': f'{year}-{month}',
    #             'excise_tax': int(value.strip().replace(',', '')),
    #         })
    
    # data = pd.DataFrame(excise_tax)
    # data = data.set_index(pd.to_datetime(data['date']))
    # data['sales'] =  data.excise_tax * 100 / TAX_RATE
    # data.plot()

    # TODO: Calculate average revenue per retailer

