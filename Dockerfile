# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local backend directory to the working directory in the container
COPY . .

# Expose port 5000 to the outside world
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "mainapp.py"]
