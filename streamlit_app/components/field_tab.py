import streamlit as st
from api.dao.field import FieldDAO

def field_tab_component(driver):

    st.title("Field Exploration")

    # Get all fields from the database
    field_dao = FieldDAO(driver)
    ids = field_dao.get_all_ids()

    # Error checking
    if not ids:
        st.error("No fields found in the database.")
        return

    # Field selection
    option = st.selectbox("Select a field to explore:", ids)
    
    # get field extra information
    field_info = field_dao.get_field_info(option)
    st.info(f"""
        **Major Land Resource Area:** {field_info['Major_Land_Resource_Area'][0]}\n
        **Postal Code:** {field_info['Postal_Code'][0]}\n
        **Established Date:** {field_info['establishedDate'][0]}\n
        **History:** {field_info['History'][0]}\n
        **Description:** {field_info['Description'][0]}\n
        **Native Vegetation:** {field_info['Native_Vegetation'][0]}\n
        **Spatial Description:** {field_info['Spatial_Description'][0]}
        """)
    
    # Column layout
    col1, col2 = st.columns(2)

    with col1:
        # Get experimental unit data
        exp_units = field_dao.get_all_experimental_unit(option)
        st.subheader("Experimental Units On Field")
        st.dataframe(exp_units, column_config={"id": "Experimental Unit Name"}, use_container_width=True, height=500)

    with col2:
        # Get latitude and longitude of the selected field
        df = field_dao.get_lat_long_dataframe(option)
        st.subheader("Field Location")
        st.map(df, latitude='latitude', longitude='longitude')

    # Rainfall data
    st.subheader("Precipitation over Time")
    rainfall_df = field_dao.get_rainfall_df(option)
    if rainfall_df is not None and not rainfall_df.empty:
        st.bar_chart(rainfall_df, x='Period', y='TotalPrecipitation')
    else:
        st.write("No rainfall data available.")
    
    # get all publicaions in a field
    publications_df = field_dao.get_publications(option)
    st.subheader("Publications on Field")
    st.dataframe(publications_df, use_container_width=True)
        
