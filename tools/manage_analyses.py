"""
Manage Analyses | Cannlytics Website
Copyright (c) 2021-2022 Cannlytics

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 12/26/2021
Updated: 1/9/2022
License: MIT License <https://github.com/cannlytics/cannlytics-website/blob/main/LICENSE>

Command-line examples:

    Get and save data.

    ```
    python tools/manage_analyses.py get_analysis_data
    ```

    Upload data.

    ```
    python tools/manage_analyses.py upload_analysis_data
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
FILENAME = 'analyses.json'
DOC = 'public/analyses'
REF = f'{DOC}/analysis_data'


def get_analysis_data():
    """Get analysis data from Firestore."""
    try:
        return get_dataset(REF, datafile=f'.datasets/{FILENAME}')
    except FileNotFoundError:
        return get_dataset(REF, datafile=f'../.datasets/{FILENAME}')


def upload_analysis_data():
    """Upload analysis data from local `.datasets`."""
    try:
        upload_dataset(f'.datasets/{FILENAME}', REF, stats_doc=DOC)
    except FileNotFoundError:
        upload_dataset(f'../.datasets/{FILENAME}', REF, stats_doc=DOC)


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
