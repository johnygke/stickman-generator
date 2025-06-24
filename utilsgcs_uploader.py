import os
from google.cloud import storage
import streamlit as st

def upload_to_gcs(local_file_path, destination_blob_name, folder_name="depression_script_1"):
    """
    Uploads a file to Google Cloud Storage inside a named folder (e.g., 'depression_script_1').

    Parameters:
        local_file_path (str): Full local path to the image.
        destination_blob_name (str): Filename only (e.g., "001.png").
        folder_name (str): Subdirectory within the GCS bucket.

    Returns:
        str: Public GCS URL if successful, else None.
    """
    try:
        bucket_name = os.getenv("GOOGLE_CLOUD_BUCKET")
        credentials_path = os.getenv("GOOGLE_CLOUD_CREDENTIALS_PATH")

        if not bucket_name or not credentials_path:
            st.error("❌ GCS config missing from .env.")
            return None

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        client = storage.Client()
        bucket = client.bucket(bucket_name)

        # Define blob path: folder_name/filename.png
        blob_path = f"{folder_name}/{destination_blob_name}"
        blob = bucket.blob(blob_path)

        blob.upload_from_filename(local_file_path)

        gcs_url = f"https://storage.googleapis.com/{bucket_name}/{blob_path}"
        st.success(f"✅ Uploaded: {gcs_url}")
        return gcs_url

    except Exception as e:
        st.error(f"❌ Upload failed: {str(e)}")
        return None
