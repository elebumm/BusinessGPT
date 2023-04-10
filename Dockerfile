# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y build-essential

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Set the environment variable for Flask
ENV FLASK_APP app.py

# Expose port 9999 for Flask to listen on
EXPOSE 9999

# Run the command to start Flask
CMD ["flask", "run", "--host=0.0.0.0"]