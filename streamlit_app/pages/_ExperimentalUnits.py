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

# Display grain yield and soil carbon storage of an experimental unit over time
# get grain yield of an experimental unit over time
grain_yield_df = exp_unit_dao.get_grain_yield(st.session_state.selected_exp_unit)
st.subheader("Grain Yield Over Time")
# check for empty dataframe
if grain_yield_df is not None and not grain_yield_df.empty:
    # remove any row that contains a null value in either column
    grain_yield_df = grain_yield_df.dropna()

    # Convert the date column to datetime
    grain_yield_df['Date'] = pd.to_datetime(grain_yield_df['Date'])
    # Ground grain yield to 2 decimal places
    grain_yield_df['grainYield'] = grain_yield_df['grainYield'].astype(float).round(2)
    # rename columns for better display
    grain_yield_df.rename(columns={
        "Date": "Date",
        "grainYield": "Grain Yield"
    }, inplace=True)
    st.line_chart(grain_yield_df, x='Date', y='Grain Yield')
else:
    st.write("No grain yield data available for this Experimental Unit.")


# get soil carbon storage of an experimental unit over time
soil_carbon_df = exp_unit_dao.get_soil_carbon(st.session_state.selected_exp_unit)

# Remove empty row if its soil carbon is None
soil_carbon_df = soil_carbon_df[soil_carbon_df['SoilCarbon'].notnull()]
# rename columns for better display
soil_carbon_df.rename(columns={
    "Date": "Date",
    "SoilCarbon": "Soil Carbon",
    "LowerDepth": "Lower Depth",
    "UpperDepth": "Upper Depth"
}, inplace=True)


st.subheader("Soil Carbon Storage Over Time")
# check for empty dataframe
if soil_carbon_df is not None and not soil_carbon_df.empty:

    # Create a new column for the depth, which is the average of the upper and lower depth
    soil_carbon_df['Average Depth'] = (soil_carbon_df['Lower Depth'] + soil_carbon_df['Upper Depth']) // 2

    # Plot the 3D soil carbon storage graph, where the x-axis is the date, y-axis is the average depth, and z-axis is the soil carbon
    figure = px.scatter_3d(soil_carbon_df, x='Date', y='Average Depth', z='Soil Carbon', color='Soil Carbon')
    st.plotly_chart(
        figure_or_data=figure,
        use_container_width=True
    )
else:
    st.write("No soil carbon data available for this Experimental Unit.")
    

# get soil chemical properties of an experimental unit over time
soil_chemical_df = exp_unit_dao.get_soil_chemical_properties(st.session_state.selected_exp_unit)
st.subheader("Other Soil Chemical Properties Over Time")
# check for empty dataframe
if soil_chemical_df is not None and not soil_chemical_df.empty:
    # remove any row that contains a null value in Date 
    soil_carbon_df = soil_carbon_df[soil_carbon_df['Date'].notnull()]

    # Convert the date column to datetime
    soil_chemical_df['Date'] = pd.to_datetime(soil_chemical_df['Date'])

    # Create a new column for the depth, which is the average of the upper and lower depth
    soil_chemical_df['Average Depth'] = (soil_chemical_df['LowerDepth'] + soil_chemical_df['UpperDepth']) // 2

    # Rename columns for better display
    soil_chemical_df.rename(columns={
        "Date": "Date",
        "Ammonium": "Ammonium",
        "Nitrate": "Nitrate",
        "PH": "pH",
        "Nitrogen": "Total Nitrogen",
    }, inplace=True)

    # 4 tabs for each soil chemical property
    tabs = st.tabs(["Ammonium", "Nitrate", "pH", "Total Nitrogen"])
    with tabs[0]:
        # check if all values in the Ammonium column are null
        if soil_chemical_df['Ammonium'].isnull().all():
            st.write("No Ammonium data available for this Experimental Unit.")
            
        else:
            figure = px.scatter_3d(soil_chemical_df, x='Date', y='Average Depth', z='Ammonium', color='Ammonium')
            st.plotly_chart(
                figure_or_data=figure,
                use_container_width=True
            )
    with tabs[1]:
        # check if all values in the Nitrate column are null
        if soil_chemical_df['Nitrate'].isnull().all():
            st.write("No Nitrate data available for this Experimental Unit.")
        else:
            figure = px.scatter_3d(soil_chemical_df, x='Date', y='Average Depth', z='Nitrate', color='Nitrate')
            st.plotly_chart(
                figure_or_data=figure,
                use_container_width=True
            )
    with tabs[2]:
        # check if all values in the pH column are null
        if soil_chemical_df['pH'].isnull().all():
            st.write("No pH data available for this Experimental Unit.")
        else:
            figure = px.scatter_3d(soil_chemical_df, x='Date', y='Average Depth', z='pH', color='pH')
            st.plotly_chart(
                figure_or_data=figure,
                use_container_width=True
            )
    with tabs[3]:
        # check if all values in the Total Nitrogen column are null
        if soil_chemical_df['Total Nitrogen'].isnull().all():
            st.write("No Total Nitrogen data available for this Experimental Unit.")
        else:
            figure = px.scatter_3d(soil_chemical_df, x='Date', y='Average Depth', z='Total Nitrogen', color='Total Nitrogen')
            st.plotly_chart(
                figure_or_data=figure,
                use_container_width=True
            )
else:
    st.write("No soil chemical data available for this Experimental Unit.")