import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Weather Forecast", layout="wide")
st.title("Weather Forecast Dashboard")

def get_weather_forecast(latitude, longitude):
    point_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    try:
        response = requests.get(point_url)
        response.raise_for_status()
        point_data = response.json()
        forecast_url = point_data["properties"]["forecast"]
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        return forecast_response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None
    
st.sidebar.header("Location Settings")
latitude = st.sidebar.number_input("Latitude", value=33.7537, format="%.4f")
longitude = st.sidebar.number_input("Longitude", value=-84.3863, format="%.4f")

if st.sidebar.button("Get Weather Forecast"):
    forecast_data = get_weather_forecast(latitude, longitude)

    if forecast_data:
        periods = forecast_data["properties"]["periods"]
        df = pd.DataFrame(periods)

        st.subheader("Temperature Forecast")
        fig_temp = px.line(df,
                           x="name",
                           y="temperature",
                           title="Temperature Forecast",
                           labels={"temperature": "Temperature (°F)", "name": "period"})
        st.plotly_chart(fig_temp)

        st.subheader("Wind Speed Forecast")
        df["wind_speed_numeric"] = df["windSpeed"].str.extract('(\d+)').astype(float)
        fig_wind = px.bar(df,
                          x="name",
                          y="wind_speed_numeric",
                          title="Wind Speed Forecast",
                          labels={"wind_speed_numeric": "Wind Speed (mph)", "name": "Period"})
        st.plotly_chart(fig_wind)

        st.subheader("Detailed Forecast")
        for period in periods:
            with st.expander(f"{period['name']} - {period['temperature']}°F"):
                st.write(f"**Wind:** {period['windSpeed']} {period['windDirection']}")
                st.write(f"**Conditions:** {period['shortForecast']}")
                st.write(f"**Detailed:** {period['detailedForecast']}")
else:
    st.info("Enter location coordinates and clock 'Get Weather Forecast' to see weather data.")