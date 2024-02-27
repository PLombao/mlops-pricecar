import os
import time
import pickle
from typing import Optional, Any

import pandas as pd
from io import StringIO
from google.cloud import storage
from google.cloud.exceptions import NotFound

def extract_bucket(bucket_name: str) -> Optional[storage.Bucket]:
    """Gets a bucket"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    return bucket


def extract_blob(source_blob_name: str, bucket_name: str) -> Optional[storage.Blob]:
    """Gets a blob from bucket"""
    bucket = extract_bucket(bucket_name)
    blob = bucket.get_blob(source_blob_name)
    if blob is None:
        raise NotFound(f'No existe el blob "{source_blob_name}".')
    return blob


def download_blob(source_blob_name: str, bucket_name: str, destination_filename: str) -> None:
    """Downloads a blob from the bucket"""
    blob = extract_blob(source_blob_name, bucket_name)
    blob.download_to_filename(destination_filename)


def upload_blob_from_file(source_filename: str, bucket_name: str, destination_base_folder: str = "", destination_filename: str = "", delete: bool = True) -> None:
    """Uploads a file to the bucket and gives the possibility to delete the file"""
    if destination_filename == "":
        modified_date = os.path.getmtime(source_filename)
        destination_filename = time.strftime("%Y%m%d%H%M%S_",time.gmtime(modified_date)) + os.path.basename(source_filename)
    
    destination_blob_name = os.path.join(destination_base_folder, destination_filename)

    bucket = extract_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_filename)
    if delete:
        os.remove(source_filename)


def get_df_from_blob_csv(source_blob_name: str, bucket_name: str) -> pd.DataFrame:
    """Downloads a csv blob from the bucket and converts it to df"""
    blob = extract_blob(source_blob_name, bucket_name)
    csv_data = blob.download_as_string()
    csv_string = csv_data.decode('utf-8')
    return pd.read_csv(StringIO(csv_string))


def get_df_from_blob_excel(source_blob_name: str, bucket_name: str) -> pd.DataFrame:
    """Downloads an excel blob from the bucket and converts it to df"""
    blob = extract_blob(source_blob_name, bucket_name)
    data_bytes = blob.download_as_bytes()
    return pd.read_excel(data_bytes)


def extract_pickle(source_blob_name: str, bucket_name: str) -> Any:
    """Extracts a blob from the bucket and unpickles it"""
    blob = extract_blob(source_blob_name, bucket_name)
    return pickle.loads(blob.download_as_string())