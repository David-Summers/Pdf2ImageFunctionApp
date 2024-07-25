

import azure.functions as func
import logging

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
    
    