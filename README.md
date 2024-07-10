# SOCKG Dashboard

SOCKG Dashboard is an interactive web application designed for the SOCK database. It offers basic visualization capabilities and natural language querying for a Neo4j database.

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

- Docker installed

## Installation

This application has been built and tested on Python 3.8. All dependencies are managed through Docker and python's requirements.txt file.

To build and run the application:

1. Clone this repository: 

2. Build and start the Docker containers:

This command will build the necessary Docker images and start the containers as defined in the `docker-compose.yml` file.

## Usage

Once the Docker build process is complete and the containers are running:

1. Open a web browser and navigate to `http://localhost:8501`
2. You should now see the SOCKG Dashboard interface
3. Use the various features for visualization and querying the SOCK database

Note: The application runs on port 8501 by default. Ensure this port is not in use by other applications on your system.

## Contributing

None for now.

## License

This project is licensed under the MIT License.