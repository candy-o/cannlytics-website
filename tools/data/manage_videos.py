"""
Manage Videos | Cannlytics Website
Copyright (c) 2021-2022 Cannlytics

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 12/26/2021
Updated: 12/27/2021
License: MIT License <https://github.com/cannlytics/cannlytics-website/blob/main/LICENSE>

Command-line examples:

    Get and save data.

    ```
    python tools/data/manage_videos.py get_video_data
    ```

    Upload data.

    ```
    python tools/data/manage_videos.py upload_video_data
    ```
"""
# Standard imports
import os
import sys

# External imports
from dotenv import dotenv_values

# Internal imports
from data_management import get_data, upload_data

# Set credentials.
try:
    config = dotenv_values('../../.env')
    credentials = config['GOOGLE_APPLICATION_CREDENTIALS']
except KeyError:
    config = dotenv_values('.env')
    credentials = config['GOOGLE_APPLICATION_CREDENTIALS']
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials


def get_video_data():
    """Get video data from Firestore."""
    ref = 'public/videos/video_data'
    try:
        return get_data(REF, datafile='.datasets/videos.json', order_by='number')
    except FileNotFoundError:
        return get_data(REF, datafile='../../.datasets/videos.json', order_by='number')


def upload_video_data():
    """Upload video data from local `.datasets`."""
    ref = 'public/videos/video_data'
    stats_doc = 'public/videos'
    try:
        upload_data('.datasets/videos.json', ref, stats_doc=stats_doc)
    except FileNotFoundError:
        upload_data('../../.datasets/videos.json', ref, stats_doc=stats_doc)


if __name__ == '__main__':

    # Make functions available from the command line.
    globals()[sys.argv[1]]()
