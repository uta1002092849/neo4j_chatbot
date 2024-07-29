import streamlit as st
import pandas as pd
from api.dao.weatherStation import weatherStationDAO

def weatherStation_tab_component(driver):

    # Custom CSS to improve appearance
    st.markdown("""
        <style>
        .big-font {
            font-size:30px !important;
            font-weight: bold;
        }
        .medium-font {
            font-size:20px !important;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Page title
    st.markdown('<p class="big-font">Weather Station Explorer</p>', unsafe_allow_html=True)
    
    # Initialize WeatherStationDAO
    weather_station_dao = weatherStationDAO(driver)
    
    # Get all weather stations from the database
    ids = weather_station_dao.get_all_ids()
    
    # Error checking
    if not ids:
        st.error("No weather stations found in the database.")
        return
    
    # Weather station selection (original box choice)
    st.markdown('<p class="medium-font">Select Weather Station</p>', unsafe_allow_html=True)
    option = st.selectbox("Choose a weather station to explore:", ids)
    
    # Main content
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown('<p class="medium-font">Weather Station Information</p>', unsafe_allow_html=True)
        weather_station_info = weather_station_dao.get_weather_station_info(option)
        located_field = weather_station_dao.get_field(option)['Field_Name'].to_list()
        located_site = weather_station_dao.get_site(option)['Site_Name'].to_list()
        
        
        st.info(f"""
        **Located on Field:** {" and ".join(located_field)}\n
        **Located on Site:** {" and ".join(located_site)}\n
        **Station Direction from Field:** {weather_station_info['Direction_From_Field'][0]}\n
        **Distance from Field:** {weather_station_info['Distance_From_Field'][0]} m\n
        **Latitude:** {weather_station_info['Latitude'][0]:.4f}\n
        **Longitude:** {weather_station_info['Longitude'][0]:.4f}
        """)
    
    with col2:
        st.markdown('<p class="medium-font">Weather Station Location</p>', unsafe_allow_html=True)
        st.map(weather_station_info, latitude='Latitude', longitude='Longitude')
    
    # Get weather observations of a weather station
    weather_observation_df = weather_station_dao.get_weather_observation(option)
    
    # Convert 'Date' column to datetime
    weather_observation_df['Date'] = pd.to_datetime(weather_observation_df['Date'], format='%Y-%m-%d')
    
    # Add separate date inputs for start and end dates
    min_date = weather_observation_df['Date'].min()
    max_date = weather_observation_df['Date'].max()
    
    # Two date inputs for start and end dates
    date_range = st.date_input(
            "**Select date range:**",
            value=[min_date, max_date],
            min_value=min_date,
            max_value=max_date,
            format="YYYY-MM-DD",
        )

    if len(date_range) != 2:
        st.stop()
    
    # Filter the DataFrame based on the selected date range
    mask = (weather_observation_df['Date'] >= pd.to_datetime(date_range[0])) & (weather_observation_df['Date'] <= pd.to_datetime(date_range[1]))
    filtered_df = weather_observation_df[mask]

    # Function to create Streamlit charts
    def create_streamlit_chart(df, x, y, title):
        st.subheader(title)
        st.line_chart(df.set_index(x)[y])
    
    # Display weather observations as charts
    st.markdown('<p class="medium-font">Weather Observations</p>', unsafe_allow_html=True)
    
    chart1, chart2 = st.columns(2)
    
    with chart1:
        create_streamlit_chart(filtered_df, 'Date', 'Open_Pan_Evaporation', "Open Pan Evaporation")
        create_streamlit_chart(filtered_df, 'Date', ['Soil_Temperature_5cm', 'Soil_Temperature_10cm'], "Soil Temperature")
    
    with chart2:
        create_streamlit_chart(filtered_df, 'Date', ['Precipitation', 'Relative_Humidity_Percent'], "Precipitation and Relative Humidity")
        create_streamlit_chart(filtered_df, 'Date', ['Solar_Radiation_Bare_Soil', 'Min_Temperature', 'Max_Temperature'], "Solar Radiation and Temperature")
    
    # Display wind speed
    create_streamlit_chart(filtered_df, 'Date', 'Wind_Speed', "Wind Speed")

    # Add a data table for detailed view
    st.markdown('<p class="medium-font">Detailed Weather Data</p>', unsafe_allow_html=True)
    st.dataframe(filtered_df.style.highlight_max(axis=0), use_container_width=True, hide_index=True, column_order=['Date', 'Open_Pan_Evaporation', 'Precipitation', 'Relative_Humidity_Percent', 'Soil_Temperature_5cm', 'Soil_Temperature_10cm', 'Solar_Radiation_Bare_Soil', 'Min_Temperature', 'Max_Temperature', 'Wind_Speed'])
