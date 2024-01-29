# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Copy requirements.txt
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 80

# Modify the CMD to use a different port (8000 instead of 80) if that's what you intended
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
