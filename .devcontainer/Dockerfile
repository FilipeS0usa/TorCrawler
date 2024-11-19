#For more images check https://github.com/devcontainers/images
FROM mcr.microsoft.com/devcontainers/python:3.11

RUN apt-get update \
    && apt-get install -y build-essential 

WORKDIR /workspace

COPY . .

WORKDIR /workspace/src

RUN pip install -r requirements.txt
