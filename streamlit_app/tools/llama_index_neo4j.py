from llama_index.tools.neo4j import Neo4jQueryToolSpec
from models.llms import gemini_pro
import streamlit as st
from llama_index.agent.openai import OpenAIAgent

db = Neo4jQueryToolSpec(
    url = st.secrets['NEO4J_URI'],
    username = st.secrets['NEO4J_USERNAME'],
    password = st.secrets['NEO4J_PASSWORD'],
    llm=gemini_pro,
)

tools = db.to_tool_list()
agent = 