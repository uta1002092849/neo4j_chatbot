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
    options = st.selectbox("Select a field to explore:", ids)

    # Column layout
    col1, col2 = st.columns(2)

    with col1:
        # Get experimental unit data
        exp_units = field_dao.get_all_experimental_unit(options)
        st.subheader("Experimental Units On Field")
        st.dataframe(exp_units)

    with col2:
        # Get latitude and longitude of the selected field
        df = field_dao.get_lat_long_dataframe(options)
        st.subheader("Field Location")
        st.map(df, latitude='latitude', longitude='longitude')

    # Rainfall data
    st.subheader("Rainfall Data Over Time")
    rainfall_df = field_dao.get_rainfall_df(options)
    if rainfall_df is not None and not rainfall_df.empty:
        st.bar_chart(rainfall_df, x='period', y='totalPrecipitation')
    else:
        st.write("No rainfall data available.")

    # Custom CSS for styling
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: auto;
        }
        .stHeader {
            text-align: center;
        }
        .stDataframe, .stTable {
            margin-top: 20px;
        }
        </style>
        """, unsafe_allow_html=True)
