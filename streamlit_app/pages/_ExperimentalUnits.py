from api.neo4j import init_driver
import streamlit as st
from api.dao.experimentalUnit import ExperimentalUnitDAO
from components.navigation_bar import navition_bar

# Page config and icon
st.set_page_config(layout="wide", page_title="SOCKG Dashboard - Experimental Unit", page_icon=":triangular_ruler:")

# sidebar for navigation
navition_bar()

# Initialize driver
driver = init_driver()

st.title("Experimental Unit Exploration")
#get all experimental units from the database
exp_unit_dao = ExperimentalUnitDAO(driver)
ids = exp_unit_dao.get_all_ids()

# error checking
if not ids:
    st.error("No experimental units found in the database.")

# initialize selected experimental unit in session state if not already initialized
if 'selected_exp_unit' not in st.session_state:
    st.session_state.selected_exp_unit = None

# Experimental unit selection
option = st.selectbox("Select an experimental unit to explore:", ids, index=None)

if option is not None:
    st.session_state.selected_exp_unit = option

# stop the script if no experimental unit is selected
if st.session_state.selected_exp_unit is None:
    st.stop()

# get all treatments applied to an experimental unit
treatments_df = exp_unit_dao.get_all_treatments(st.session_state.selected_exp_unit)
st.subheader("Treatments Applied")
st.dataframe(treatments_df, use_container_width=True)

col1, col2 = st.columns(2)


with col1:
    # get grain yield of an experimental unit over time
    grain_yield_df = exp_unit_dao.get_grain_yield(st.session_state.selected_exp_unit)
    st.subheader("Grain Yield Over Time")
    # check for empty dataframe
    if grain_yield_df is not None and not grain_yield_df.empty:
        st.line_chart(grain_yield_df, x='Date', y='grainYield')
    else:
        st.write("No grain yield data available for this Experimental Unit.")

with col2:
    # get soil carbon storage of an experimental unit over time
    soil_carbon_df = exp_unit_dao.get_soil_carbon(st.session_state.selected_exp_unit)
    st.subheader("Soil Carbon Storage Over Time")
    # check for empty dataframe
    if soil_carbon_df is not None and not soil_carbon_df.empty:
        st.bar_chart(soil_carbon_df, x='Date', y='SoilCarbon')
    else:
        st.write("No soil carbon data available for this Experimental Unit.")
    

# get soil chemical properties of an experimental unit over time
soil_chemical_df = exp_unit_dao.get_soil_chemical_properties(st.session_state.selected_exp_unit)
st.subheader("Soil Chemical Properties Over Time")
# check for empty dataframe
if soil_chemical_df is not None and not soil_chemical_df.empty:
    on = st.toggle("Line Chart", False)
    if on:
        st.line_chart(soil_chemical_df, x='Date', y=['Ammonium', 'Nitrate', 'PH', 'Nitrogen'])
    else:
        st.dataframe(soil_chemical_df, use_container_width=True)
    
else:
    st.write("No soil chemical data available for this Experimental Unit.")