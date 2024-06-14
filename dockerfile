# use prebuilt image with llama3
FROM python:3.10-slim

# update and install curl
RUN apt-get update && apt-get install git -y && apt-get install curl -y

# install ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# dowbload llama3 7B model
RUN ollama pull llama3

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "dashboard.py"]