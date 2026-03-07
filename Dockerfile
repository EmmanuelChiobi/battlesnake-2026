FROM ubuntu:24.04
FROM python:3.10.6-slim

# Install app
COPY . /usr/app
WORKDIR /usr/app

# Install dependencies
RUN apt-get update && apt-get upgrade
RUN pip install --upgrade pip && pip install -r requirements.txt

# Run Battlesnake
CMD [ "python", "main.py" ]
