import azure.functions as func
import logging
from azure.storage.blob import BlobServiceClient, ContainerClient
from process import process_file

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ProcessPDF")
def ProcessPDF(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Extract parameters from query
    url = req.params.get('url')
    CONNECTION_STRING = req.params.get('connectionString')
    CONTAINER_NAME = req.params.get('containerName')

    # Optionally, handle case where parameters might be in the request body
    try:
        req_body = req.get_json()
    except ValueError:
        req_body = {}
    
    url = url or req_body.get('url')
    CONNECTION_STRING = CONNECTION_STRING or req_body.get('connectionString')
    CONTAINER_NAME = CONTAINER_NAME or req_body.get('containerName')

    # Validate required parameters
    if not all([url, CONNECTION_STRING, CONTAINER_NAME]):
        return func.HttpResponse(
            "Missing required parameters: url, connectionString, containerName",
            status_code=400
        )

    # Ensure connection string is a string
    if isinstance(CONNECTION_STRING, dict):
        CONNECTION_STRING = CONNECTION_STRING.get('WebUrl', '')

    # Validate that CONNECTION_STRING is now a string
    if not isinstance(CONNECTION_STRING, str):
        return func.HttpResponse(
            "Invalid connectionString parameter format.",
            status_code=400
        )

    # Convert CONTAINER_NAME to lowercase
    CONTAINER_NAME = CONTAINER_NAME.lower()

    # Create the container in Blob Storage if it doesn't exist
    try:
        blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        if not container_client.exists():
            container_client.create_container()
            logging.info(f"Container '{CONTAINER_NAME}' created.")
        else:
            logging.info(f"Container '{CONTAINER_NAME}' already exists.")
    except Exception as e:
        logging.error(f"Error creating container: {e}")
        return func.HttpResponse(
            f"Error creating container: {e}",
            status_code=500
        )

    try:
        process_file(url, CONTAINER_NAME, CONNECTION_STRING)

        return func.HttpResponse(
            "This HTTP triggered function executed successfully.",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return func.HttpResponse(
            "An error occurred processing your request.",
            status_code=500
        )
