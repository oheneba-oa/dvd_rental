# Use a lightweight Python image
FROM python:3.11-slim

# Set the working folder inside the container
WORKDIR /app

# Copy the requirements file first
COPY requirements.txt .

# Install the Python libraries listed in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Keep the container ready for manual commands while building/testing
CMD ["bash"]