# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
ADD src /app 

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the src/app directory into the container at /app
COPY src/app /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /tmp

# Install any needed packages specified in requirements.txt
RUN pip install -r /tmp/requirements.txt

# Set environment variable for Flask app
ENV FLASK_APP=/app

# Expose the port that Flask will run on
EXPOSE 5000

# Define the command to run on container start
CMD ["flask", "run", "--host", "0.0.0.0"]
