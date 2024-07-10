# SOCKG Dashboard

SOCKG Dashboard is an interactive web application designed for the SOCK database. It provides basic visualization capabilities and natural language querying for a Neo4j database.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Interactive web interface
- Basic data visualization
- Natural language querying for Neo4j database

## Prerequisites

- Docker installed on your system

## Installation

This application is built and tested on Python 3.8. All dependencies are managed through Docker and a Python requirements.txt file.

To set up and run the application:

1. Clone the repository:
```
$ git clone https://github.com/uta1002092849/neo4j_chatbot.git
```

2. Configure API key and Neo4j credentials:
- Navigate to `streamlit_app/.streamlit/`
- Create a file named `secrets.toml`
- Add the following configurations to `secrets.toml`:
```
  API_KEY = "<your gemini api key>"
  MODEL = "<llm model>"

  NEO4J_URI = "bolt://idir.uta.edu:7687"
  NEO4J_USERNAME = "<your sockg username>"
  NEO4J_PASSWORD = "<your sockg password>"
```

3. Build and start the Docker containers:
```
sudo docker compose up
```
This command builds the necessary Docker images and starts the containers as defined in the `docker-compose.yml` file.

## Usage

After the Docker build process completes and containers are running:

1. Open a web browser and go to `http://localhost:8501`
2. You will see the SOCKG Dashboard interface
3. Use the features for visualization and querying the SOCK database

Note: The application runs on port 8501 by default. Ensure this port is not in use by other applications on your system.

## Contributing

No contributions are currently being accepted.

## License

This project is licensed under the MIT License.



