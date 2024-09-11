import requests
import pdf2image
import tempfile
import os
import sys

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def upload_file_to_blob(file_path, container_name, blob_name, connection_string):
    # Create a BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    # Get a reference to the container and create it if it doesn't exist
    container_client = blob_service_client.get_container_client(container_name)
    if not container_client.exists():
        container_client.create_container()
    
    # Create a BlobClient to interact with the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    # Upload the file
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    print(f"File {file_path} uploaded to {container_name}/{blob_name}")

def upload_images_to_blob(images, container_name, connection_string):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    for index, image in enumerate(images):
        # Create a temporary file for the image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
            image.save(temp_image, format="JPEG")
            temp_image_path = temp_image.name
        
        # Define a unique blob name
        blob_name = f"uploaded_image_{index}.jpg"
        
        # Upload the temporary image file to Azure Blob Storage
        upload_file_to_blob(temp_image_path, container_name, blob_name, connection_string)
        
        # Delete the temporary file
        os.remove(temp_image_path)
        print(f"Image {index} uploaded to {container_name}/{blob_name}")

def process_file(url, image_container_name, image_connection_string):

    #response = requests.get(url)
    #print(response.content)

    CONTAINER_NAME = "upload"
    blob_name = url.split("/").pop()

    blob_service_client = BlobServiceClient.from_connection_string(image_connection_string)
    blob_client = blob_service_client.get_blob_client(container = CONTAINER_NAME, blob = blob_name)
    blob_data = blob_client.download_blob()
    pdf_stream = blob_data.content_as_bytes()

    images = pdf2image.convert_from_bytes(pdf_stream)

    #with open('file.pdf', 'wb') as f:
    #    f.write(blob_data.content_as_bytes())

    
    upload_images_to_blob(images, image_container_name, image_connection_string)




