# Use the official Python 3.11.6 (slim) image
FROM python:3.11.6-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Update the package list and install necessary packages
RUN apt-get update && \
    apt-get -y install supervisor

RUN apt-get update && \
    apt-get -y install nginx

# RUN apt-get update && \
#     apt-get -y install gcc

# Copy Nginx configuration to the container
COPY ./docker/config/nginx/app.conf /etc/nginx/sites-enabled/app.conf

# Copy Supervisor configuration to the container
COPY ./docker/config/supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Create the log and run directories for supervisord
RUN mkdir -p /var/log/supervisord /var/run/supervisord

# Set the working directory
WORKDIR /var/www/app

# Copy requirements.txt and Pipfile.lock to the container
COPY Pipfile.lock /var/www/app/

# Install project dependencies using pip and pipenv
RUN pip install pipenv
RUN pipenv install --ignore-pipfile --verbose

# Copy the rest of your project files to the container
COPY . .

# Expose the port if your Django project uses it
EXPOSE 8000

CMD supervisord -n -c /etc/supervisor/conf.d/supervisord.conf