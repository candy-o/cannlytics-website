"""
Upload File to Firebase Storage | Cannlytics Website
Copyright (c) 2021-2022 Cannlytics

Authors: Keegan Skeate <keegan@cannlytics.com>
Created: 1/22/2022
Updated: 1/22/2022
License: MIT License <https://github.com/cannlytics/cannlytics-website/blob/main/LICENSE>

Command-line example:

    ```
    python tools/firebase/upload_file.py {ref} {file}
    ```

"""
# Standard imports.
from datetime import datetime
import os
import sys

# External imports.
from dotenv import dotenv_values

# Internal imports.
sys.path.append('../../')
sys.path.append('./')
from cannlytics.firebase import ( # pylint: disable=import-error, wrong-import-position
    get_file_url,
    initialize_firebase,
    upload_file,
)


def upload_file_to_storage(ref: str, file_name: str) -> str:
    """Set the `updated_at` field on all documents in a collection.
    Args:
        ref (str): The location for the file.
        file_name (str): The full file name of the file to upload.
    Returns:
        (str): Returns a URL link ot the file.
    """
    print('Uploading file to ', ref)
    bucket = config['FIREBASE_STORAGE_BUCKET']
    upload_file(ref, file_name, bucket_name=bucket)
    file_url = get_file_url(ref, bucket_name=bucket)
    print('File uploaded. Link:', file_url)
    return file_url


if __name__ == '__main__':

    # Initialize Firebase.
    try:
        config = dotenv_values('../../.env')
        credentials = config['GOOGLE_APPLICATION_CREDENTIALS']
    except KeyError:
        config = dotenv_values('.env')
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials
    initialize_firebase()

    # Update all docs in a given collection.
    ref = sys.argv[1]
    file_name = sys.argv[2]
    upload_file_to_storage(ref, file_name)
