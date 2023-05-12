# Author: Joseph
# Brief: This file defines how the docker image is built. 

# This base image includes pip3!
FROM python:3.11.3

# Set the django folder inside the container as the workdir
WORKDIR /django/

# Copy requirements.txt from this directory into the workdir
COPY requirements.txt .

# Install dependencies.
# (--no-cache-dir) => Do not use the cache directory for storing downloaded package files. This it avoid any
# caching errors, and enhance reproducibility. 
# (-r requirements.txt) => Tell pip to read and install the dependencies inside of the requirements.txt file.
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy everything inside this directory and move it to the container's workdir.
COPY . .