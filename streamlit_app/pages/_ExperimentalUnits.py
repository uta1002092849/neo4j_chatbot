from api.neo4j import init_driver
import streamlit as st
from api.dao.experimentalUnit import ExperimentalUnitDAO
from components.navigation_bar import navition_bar
import pandas as pd
import plotly.express as px

# Page config and icon
st.set_page_config(layout="wide", page_title="SOCKG Dashboard - Experimental Unit", page_icon=":triangular_ruler:")

# sidebar for navigation
navition_bar()

# Initialize driver
driver = init_driver()

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Experimental Unit Exploration</h1>", unsafe_allow_html=True)
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
st.subheader("Select an Experimental Unit:")
option = st.selectbox("Select an experimental unit to explore:", ids, index=None, label_visibility="collapsed")

if option is not None:
    st.session_state.selected_exp_unit = option

# stop the script if no experimental unit is selected
if st.session_state.selected_exp_unit is None:
    st.stop()
    
# Fetch and Display information about the selected experimental unit
experimental_unit_info = exp_unit_dao.get_exp_unit_info(st.session_state.selected_exp_unit)
st.info(f"""
    **Experimental Unit ID:** {experimental_unit_info['ID'][0]}\n
    **Description:** {experimental_unit_info['Description'][0] if str(experimental_unit_info['Description'][0]) != 'nan' else "Unavailable"}\n
    **Start Date:** {experimental_unit_info['Start_Date'][0] if str(experimental_unit_info['Start_Date'][0]) != 'nan' else "Unavailable"}\n
    **End Date:** {experimental_unit_info['End_Date'][0] if str(experimental_unit_info['End_Date'][0]) != 'nan' else "Present"}\n
    **Size:** {experimental_unit_info['Size'][0]}\n
    **Field Slope Percent:** {experimental_unit_info['SlopePercent'][0]}\n
    **Landscape Position:** {experimental_unit_info['LandscapePosition'][0]}
    """)

# get all treatments applied to an experimental unit
treatments_df = exp_unit_dao.get_all_treatments(st.session_state.selected_exp_unit)
st.subheader("Treatments Applied")

# Rename columns for better display
treatments_df.rename(columns={
    "Name": "Name",
    "Start_Date": "Start Date",
    "End_Date": "End Date"
}, inplace=True)

# Change end date to 'Present' if it is empty
treatments_df['End Date'] = treatments_df['End Date'].apply(lambda x: 'Present' if pd.isnull(x) else x)
events = st.dataframe(
    treatments_df, 
    use_container_width=True,
    on_select='rerun',
    selection_mode='single-row',
    hide_index=True
    )

# Display the selected treatment details
selected_row = events.selection.rows
if selected_row:
    st.session_state.selected_treatment = treatments_df.loc[selected_row[0], "ID"]
    st.switch_page("pages/_Treatments.py")

st.subheader("Grain Yield Over Time")
grain_yield_df = exp_unit_dao.get_grain_yield(st.session_state.selected_exp_unit)
if grain_yield_df is not None and not grain_yield_df.empty:
    grain_yield_df = grain_yield_df.dropna()
    grain_yield_df['Date'] = pd.to_datetime(grain_yield_df['Date'])
    grain_yield_df['grainYield'] = grain_yield_df['grainYield'].astype(float).round(2)
    grain_yield_df.rename(columns={"Date": "Date", "grainYield": "Grain Yield"}, inplace=True)
    
    tab1, tab2 = st.tabs(["Chart", "Data"])
    with tab1:
        st.line_chart(grain_yield_df, x='Date', y='Grain Yield')
    with tab2:
        avg_yield = grain_yield_df['Grain Yield'].mean()
        min_yield = grain_yield_df['Grain Yield'].min()
        max_yield = grain_yield_df['Grain Yield'].max()
        
        cols = st.columns(3)
        with cols[0]:
            st.metric("Average Yield", f"{avg_yield:.2f}")
        with cols[1]:
            st.metric("Minimum Yield", f"{min_yield:.2f}")
        with cols[2]:
            st.metric("Maximum Yield", f"{max_yield:.2f}")
        
        st.dataframe(grain_yield_df.style.highlight_max(axis=0), use_container_width=True, hide_index=True)
else:
    st.write("No grain yield data available for this Experimental Unit.")

st.subheader("Soil Carbon Storage Over Time")
soil_carbon_df = exp_unit_dao.get_soil_carbon(st.session_state.selected_exp_unit)
soil_carbon_df = soil_carbon_df[soil_carbon_df['SoilCarbon'].notnull()]
soil_carbon_df.rename(columns={
    "Date": "Date", "SoilCarbon": "Soil Carbon",
    "LowerDepth": "Lower Depth", "UpperDepth": "Upper Depth"
}, inplace=True)

if soil_carbon_df is not None and not soil_carbon_df.empty:
    soil_carbon_df['Average Depth'] = (soil_carbon_df['Lower Depth'] + soil_carbon_df['Upper Depth']) // 2
    
    tab1, tab2 = st.tabs(["Chart", "Data"])
    with tab1:
        figure = px.scatter_3d(soil_carbon_df, x='Date', y='Average Depth', z='Soil Carbon', color='Soil Carbon')
        st.plotly_chart(figure, use_container_width=True)
    with tab2:
        avg_carbon = soil_carbon_df['Soil Carbon'].mean()
        min_carbon = soil_carbon_df['Soil Carbon'].min()
        max_carbon = soil_carbon_df['Soil Carbon'].max()
        cols = st.columns(3)
        with cols[0]:
            st.metric("Average Soil Carbon", f"{avg_carbon:.2f}")
        with cols[1]:
            st.metric("Minimum Soil Carbon", f"{min_carbon:.2f}")
        with cols[2]:
            st.metric("Maximum Soil Carbon", f"{max_carbon:.2f}")
        
        st.dataframe(soil_carbon_df.style.highlight_max(axis=0), use_container_width=True, hide_index=True)
else:
    st.write("No soil carbon data available for this Experimental Unit.")

st.subheader("Other Soil Chemical Properties Over Time")
soil_chemical_df = exp_unit_dao.get_soil_chemical_properties(st.session_state.selected_exp_unit)
if soil_chemical_df is not None and not soil_chemical_df.empty:
    soil_chemical_df = soil_chemical_df[soil_chemical_df['Date'].notnull()]
    soil_chemical_df['Date'] = pd.to_datetime(soil_chemical_df['Date'])
    soil_chemical_df['Average Depth'] = (soil_chemical_df['LowerDepth'] + soil_chemical_df['UpperDepth']) // 2
    soil_chemical_df.rename(columns={
        "Date": "Date", "Ammonium": "Ammonium", "Nitrate": "Nitrate",
        "PH": "pH", "Nitrogen": "Total Nitrogen",
    }, inplace=True)

    col1, col2 = st.columns(2)
    properties = ["Ammonium", "Nitrate", "pH", "Total Nitrogen"]
    
    for i, prop in enumerate(properties):
        with col1 if i % 2 == 0 else col2:
            st.subheader(prop)
            if soil_chemical_df[prop].isnull().all():
                st.write(f"No {prop} data available for this Experimental Unit.")
            else:
                tab1, tab2 = st.tabs(["Chart", "Data"])
                with tab1:
                    figure = px.scatter_3d(soil_chemical_df, x='Date', y='Average Depth', z=prop, color=prop)
                    st.plotly_chart(figure, use_container_width=True)
                with tab2:
                    avg_value = soil_chemical_df[prop].mean()
                    min_value = soil_chemical_df[prop].min()
                    max_value = soil_chemical_df[prop].max()

                    cols = st.columns(3)
                    
                    with cols[0]:
                        st.metric(f"Average {prop}", f"{avg_value:.2f}")
                    with cols[1]:
                        st.metric(f"Minimum {prop}", f"{min_value:.2f}")
                    with cols[2]:
                        st.metric(f"Maximum {prop}", f"{max_value:.2f}")
                    
                    st.dataframe(soil_chemical_df[['Date', 'Average Depth', prop]].style.highlight_max(axis=0), use_container_width=True, hide_index=True)
else:
    st.write("No soil chemical data available for this Experimental Unit.")