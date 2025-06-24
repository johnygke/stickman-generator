
import os
from google.cloud import storage

def upload_to_gcs(local_file_path, destination_blob_name, bucket_name=None):
    try:
        if not bucket_name:
            bucket_name = os.getenv("GCS_BUCKET_NAME")
        credentials_path = os.getenv("GOOGLE_CLOUD_CREDENTIALS_PATH")
        storage_client = storage.Client.from_service_account_json(credentials_path)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(local_file_path)
        return f"gs://{bucket_name}/{destination_blob_name}"
    except Exception as e:
        print(f"[Upload Failed] {str(e)}")
        return None
