# SOCKG Dashboard

SOCKG Dashboard is an interactive web application designed for the SOCKG (Soil Organic Carbon Knowledge Graph). It provides visual display of key information as well as natural language querying the knowledge graph.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Key Components](#key-components)
- [License](#license)

## Features

- **Interactive Web Interface**: Built with Streamlit.
- **Data Visualization**: Visualize key classes such as Field, Experimental Unit, Treatment, ...
- **Natural Language Querying**: Query the Neo4j knowledge graph using natural language.

## Prerequisites

- Docker installed on your system (version 27.1.1 is tested)
- Since this project make use llama3:7b. 16GB of memory and a GPU available machine is recommmend

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
  NEO4J_USERNAME = "<your sockg username>"    # Contact IDIR lab for credentials
  NEO4J_PASSWORD = "<your sockg password>"    # Contact IDIR lab for credentials
  MAP_BOX_API = <Your mapbox api key>         # Obtain for free on mapbox.com
```

3. Build and start the Docker containers:
```
docker compose up
```
This command builds the necessary Docker images and starts the containers as defined in the `docker-compose.yml` file.

## Usage

After the Docker build process completes and containers are running:

1. Open your web browser and go to `http://localhost:8501`
2. Explore the SOCKG Dashboard web interface.
3. Use the features for visualization and querying the SOCKG database

Note: The application runs on port 8501 by default. Ensure this port is not in use by other applications on your system.

## Directory Structure
The project is organized as follows:
```
/project-root
├── streamlit_app/        # Source code for the application
│   ├── .streamlit        # Configuration directory (e.g., secrets.toml)
│   ├── collected_datas/  # Store User ratings for question-generated cypher pairs
│   │   └── ....json
│   ├── componets/        # Reusable visualization components
│   |   └── ...
|   ├── models/           # LangChain objects for LLMs and embeddings
|   ├── neo4j-connector   # Neo4j driver initialization
|   ├── pages/            # Streamlit pages (e.g., /Fields, /Treatment)
|   ├── templates/        # LLM prompt templates
|   └── tools/            # LangChain tools for few-shot (RAG) agents
|
├── Docker-compose.yaml   # Docker Compose specification
└── README.md             # Project overview
```

## Keys Componets
1. Front End: Built using Streamlit, with use of data processing and visualization libraries (Pandas, Plotly, Pydeck). The web app is structured into multiple subpages, each allowing users to select a key identifier (ID) of a class and retrieve related information through various visual elements like charts, tables, and graphs. The "Text2Cypher" subpage enables natural language querying of the knowledge graph, using Llama3.
Text2Cypher is one the subpages that allows user to query the knowledge graph using natural language. It is built on llama3 using dynamically selected few shot examples (emebedding for each fair is generated using llama3)
2. Back End: The SOCKG knowledge graph is hosted at idir.uta.edu, while the LLaMA3 model runs locally on your machine.

## License
This project is licensed under the MIT License.