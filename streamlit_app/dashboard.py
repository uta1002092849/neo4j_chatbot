import streamlit as st
from components.navigation_bar import navition_bar

# Page config and icon
st.set_page_config(layout="wide", page_title="SOCKG Dashboard", page_icon=":seedling:")

# sidebar for navigation
navition_bar()

st.title("Welcome to SOCKG Dashboard")
st.write("Use the sidebar to navigate through the different sections of the dashboard.")
