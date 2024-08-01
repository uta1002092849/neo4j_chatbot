import streamlit as st

def navition_bar():
    st.sidebar.title("Navigation")
    with st.sidebar:
        st.page_link("dashboard.py", label="Home", icon="🏡")
        st.page_link("pages/_Fields.py", label="Field Explorer", icon="🏞️")
        st.page_link("pages/_ExperimentalUnits.py", label="Experimental Unit Explorer", icon="📐")
        st.page_link("pages/_Treatments.py", label="Treatment Explorer", icon="💊")
        st.page_link("pages/_WeatherStations.py", label="Weather Station Explorer", icon="🌡️")
        st.page_link("pages/_Text2Cypher.py", label="Text2Cypher", icon="⌨️")