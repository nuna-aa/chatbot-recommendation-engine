# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Copy the current directory contents into the container at /app
COPY ./src /app/src
COPY ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r /app/requirements.txt

# Set the working directory to /app
WORKDIR /app/src

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]