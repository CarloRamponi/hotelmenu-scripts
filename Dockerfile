
# Use the official Python base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main script to the container
COPY src/ .
COPY grafiche/ ./grafiche

# Set the entrypoint command to execute the main script
ENTRYPOINT ["python", "hotelmenu.py"]
