"""
Manage Lab Data | Cannlytics Website
Copyright (c) 2022 Cannlytics

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 1/9/2022
Updated: 1/9/2022
License: MIT License <https://github.com/cannlytics/cannlytics-website/blob/main/LICENSE>

Command-line examples:

    Get and save data.

    ```
    python tools/manage_labs.py get_lab_data
    ```

    Upload data.

    ```
    python tools/manage_labs.py upload_lab_data
    ```
"""
# Standard imports.
import os
import sys

# External imports.
from dotenv import dotenv_values

# Internal imports.
from datasets import get_dataset, upload_dataset

# Define references.
FILENAME = 'labs.json'
DOC = 'public/data'
REF = f'{DOC}/labs'
ID = 'license'


def get_lab_data():
    """Get lab data from Firestore."""
    try:
        return get_dataset(REF, datafile=f'.datasets/{FILENAME}')
    except FileNotFoundError:
        return get_dataset(REF, datafile=f'../.datasets/{FILENAME}')


def upload_lab_data():
    """Upload lab data from local `.datasets`."""
    try:
        upload_dataset(f'.datasets/{FILENAME}', REF, id_key=ID, stats_doc=DOC)
    except FileNotFoundError:
        upload_dataset(f'../.datasets/{FILENAME}', REF, id_key=ID, stats_doc=DOC)


if __name__ == '__main__':

    # Set credentials.
    try:
        config = dotenv_values('../.env')
        credentials = config['GOOGLE_APPLICATION_CREDENTIALS']
    except KeyError:
        config = dotenv_values('.env')
        credentials = config['GOOGLE_APPLICATION_CREDENTIALS']
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials

    # Call function from the command line.
    globals()[sys.argv[1]]()
