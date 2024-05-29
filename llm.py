import streamlit as st
from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(
    google_api_key = st.secrets['API_KEY'],
    model= st.secrets['MODEL']
)
