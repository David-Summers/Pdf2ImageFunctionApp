# To enable ssh & remote debugging on app service change the base image to the one below
# FROM mcr.microsoft.com/azure-functions/python:4-python3.11-appservice
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

ENV FUNCTIONS_WORKER_RUNTIME="python"
ENV AzureWebJobsFeatureFlags="EnableWorkerIndexing"
COPY requirements.txt /
RUN pip install -r /requirements.txt

RUN apt-get update -y
RUN apt-get install poppler-utils -y


COPY . /home/site/wwwroot