import streamlit as st
from langchain_community.graphs.neo4j_graph import Neo4jGraph

graph = Neo4jGraph(
    url = st.secrets['NEO4J_URI'],
    username = st.secrets['NEO4J_USERNAME'],
    password = st.secrets['NEO4J_PASSWORD']
)