# use prebuilt image with Python 3.10
FROM python:3.10-slim

# update and install git and curl
RUN apt-get update && apt-get install -y git curl

# install ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Pull llama3
CMD ollama serve && ollama run llama3

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# # Run app.py when the container launches (this will be passed as an argument to start_services.sh)
# CMD ["streamlit", "run", "dashboard.py"]