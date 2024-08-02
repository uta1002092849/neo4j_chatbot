from api.neo4j import init_driver
import streamlit as st
from api.dao.field import FieldDAO
from components.navigation_bar import navition_bar

# Page config and icon
st.set_page_config(layout="wide", page_title="SOCKG Dashboard - Fields", page_icon=":national_park:")

# sidebar for navigation
navition_bar()

# Initialize driver
driver = init_driver()

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Field Exploration</h1>", unsafe_allow_html=True)
# Get all fields from the database
field_dao = FieldDAO(driver)
ids = field_dao.get_all_ids()

# Error checking
if not ids:
    st.error("No fields found in the database.")

# initialize selected field in session state if not already initialized
if 'selected_field' not in st.session_state:
    st.session_state.selected_field = None

# Field selection
st.subheader("Select a Field:")
option = st.selectbox("Select a field to explore:", ids, index=None, label_visibility="collapsed")
if option is not None:
    st.session_state['selected_field'] = option

# get field extra information
if st.session_state.selected_field is None:
    st.stop()

field_info = field_dao.get_field_info(st.session_state.selected_field)
st.info(f"""
    **Major Land Resource Area:** {field_info['Major_Land_Resource_Area'][0]}\n
    **Postal Code:** {field_info['Postal_Code'][0] if str(field_info['Postal_Code'][0]) != "nan" else "Not available"}\n
    **Established Date:** {field_info['establishedDate'][0]}\n
    **History:** {field_info['History'][0]}\n
    **Description:** {field_info['Description'][0] if field_info['Description'][0] != None else "Not available"}\n
    **Native Vegetation:** {field_info['Native_Vegetation'][0]}\n
    **Spatial Description:** {field_info['Spatial_Description'][0] if str(field_info['Spatial_Description'][0]) != "nan" else "Not available"}\n
    """)

# Column layout
col1, col2 = st.columns(2)

with col1:
    # Get experimental unit data
    exp_units = field_dao.get_all_experimental_unit(st.session_state.selected_field)
    st.subheader("Experimental Units On Field")
    st.dataframe(exp_units, column_config={"id": "Experimental Unit Name"}, use_container_width=True, height=500)

with col2:
    # Get latitude and longitude of the selected field
    df = field_dao.get_lat_long_dataframe(st.session_state.selected_field)
    st.subheader("Field Location")
    st.map(df, latitude='latitude', longitude='longitude')

# Rainfall data
st.subheader("Precipitation over Time")
rainfall_df = field_dao.get_rainfall_df(st.session_state.selected_field)
if rainfall_df is not None and not rainfall_df.empty:
    st.bar_chart(rainfall_df, x='Period', y='TotalPrecipitation')
else:
    st.write("No rainfall data available.")

# get all publicaions in a field
publications_df = field_dao.get_publications(st.session_state.selected_field)
st.subheader("Publications on Field")
st.dataframe(publications_df, use_container_width=True)