

import azure.functions as func
import logging

from process import process_file

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="ProcessPDF")
def ProcessPDF(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # url =  'https://todelpythonipload.blob.core.windows.net/upload/Combined-MC_CoE_SCAN_POS_20240311_001%20(1).pdf?sp=r&st=2024-07-24T23:32:37Z&se=2025-07-25T07:32:37Z&spr=https&sv=2022-11-02&sr=b&sig=Iq%2FWp1jgG%2FsRHUK%2FAvLUpvxFV1ZQddGNB2YukGPSmdU%3D'
    # CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=todelpythonipload;AccountKey=jrhJ9j83zIoxm8/QrNbKBN9XrHs7KzRGtX24R9iM2xS1ddmwbRVuWd3eJ+XZ5v6kp3Zejfgb+Bcx+AStgIzydg==;EndpointSuffix=core.windows.net"
    # CONTAINER_NAME = "images"

    # Extract parameters from query
    url = req.params.get('url')
    CONNECTION_STRING = req.params.get('connectionString')
    CONTAINER_NAME = req.params.get('containerName')

    # Optionally, handle case where parameters might be in the request body
    try:
        req_body = req.get_json()
    except ValueError:
        pass
    else:
        url = url or req_body.get('url')
        CONNECTION_STRING = CONNECTION_STRING or req_body.get('connectionString')
        CONTAINER_NAME = CONTAINER_NAME or req_body.get('containerName')

    # Validate required parameters
    if not all([url, CONNECTION_STRING, CONTAINER_NAME]):
        return func.HttpResponse(
            "Missing required parameters: url, connectionString, containerName",
            status_code=400
        )

    try:
        process_file(url, CONTAINER_NAME, CONNECTION_STRING)

        return func.HttpResponse(
            "This HTTP triggered function executed successfully.",
            status_code=200)
    except Exception as e:
        return func.HttpResponse(
            "An error occurred processing your request.",
            status_code=500
        )
    
    