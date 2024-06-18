# Use prebuilt image with Python 3.10
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Update and install git and curl
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Make healthcheck available
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Make entry_point.sh executable
RUN chmod +x /app/entry_point.sh

# Run entry_point.sh when the container launches
ENTRYPOINT ["/app/entry_point.sh"]
