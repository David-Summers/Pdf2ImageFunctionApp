# What this does

This is an app function written in python that takes a pdf file and converts it into an image.

It takes 3 variables

- url - the url of the pdf file (can be an SAS token from a blob storage)
- connectionString - the connection string to the blob storage which will store the images
- containerName - the name of the container which will store the images

A sample URL could be - 
http://localhost:7075/api/ProcessPDF?url=[url]connectionString=[connectionString]&containerName=images

Make sure the url is encoded properly. 


# Build process


# Deployment process

The build process involves creating a docker image and pushing it to an azure container registry. Then pointing an azure function to the image in the container registry.

# How to use

- Use az login to log into your azure tenant  
- goto  deploy.azcli  
- replace uniqueStr with your own value  
- run sh deploy.azcli





