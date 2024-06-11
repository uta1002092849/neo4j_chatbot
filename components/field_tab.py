import streamlit as st
from api.dao.field import FieldDAO

def field_tab_component(driver):
    st.write("Fields")

    # Get all fields from the database
    field_dao = FieldDAO(driver)
    fields = field_dao.get_all_ids()

    option = st.selectbox("Select a field to explore:", fields)

    # Get experimental unit data
    exp_units = field_dao.get_all_experimental_unit(option)
    st.write("Total experimental units:", len(exp_units))

    # print out a table of experimental units
    st.dataframe(exp_units)
    
    # Get latitude and longitude of the selected field
    df = field_dao.get_lat_long_dataframe(option)
    
    # map
    st.map(df, latitude='latitude', longitude='longitude')

    # get rainfall data
    rainfall_df = field_dao.get_rainfall_df(option)
    st.bar_chart(rainfall_df, x='period', y='totalPrecipitation')
