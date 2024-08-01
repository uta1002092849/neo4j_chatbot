import streamlit as st

# Page config and icon
st.set_page_config(layout="wide", page_title="SOCKG Dashboard", page_icon=":seedling:")

# sidebar for navigation
st.sidebar.title("Navigation")
with st.sidebar:
    st.page_link("dashboard.py", label="Home", icon="🏡")
    st.page_link("pages/_Fields.py", label="Field Explorer", icon="🏞️")
    st.page_link("pages/_ExperimentalUnits.py", label="Experimental Unit Explorer", icon="📐")
    st.page_link("pages/_Treatments.py", label="Treatment Explorer", icon="💊")
    st.page_link("pages/_WeatherStations.py", label="Weather Station Explorer", icon="🌡️")
    st.page_link("pages/_Text2Cypher.py", label="Text2Cypher", icon="⌨️")

st.title("Welcome to SOCKG Dashboard")
st.write("Use the sidebar to navigate through the different sections of the dashboard.")
