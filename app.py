# Created by Jareer Shafiq

import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config FIRST
st.set_page_config(page_title="Weather App", page_icon="☁️", layout="wide")

# Predefined weather data for demo
weather_data = {
    "Karachi": {"temp": 28, "humidity": 65, "wind": 10, "pressure": 1012},
    "Lahore": {"temp": 30, "humidity": 55, "wind": 12, "pressure": 1010},
    "Islamabad": {"temp": 26, "humidity": 50, "wind": 8, "pressure": 1015},
    "New York": {"temp": 15, "humidity": 60, "wind": 5, "pressure": 1020},
    "London": {"temp": 10, "humidity": 70, "wind": 6, "pressure": 1018},
}

# Custom CSS & Theme Selection
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark", "Modern"])

st.markdown("""
    <style>
    .welcome-box { text-align: center; padding: 20px; font-size: 26px; font-weight: bold; background: linear-gradient(90deg, #ff8a00, #e52e71); color: white; border-radius: 10px; }
    .main-container { padding: 20px; border-radius: 12px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); }
    .metric-box { border-radius: 8px; padding: 10px; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# Streamlit UI
st.markdown("<div class='welcome-box'>🌎 Welcome to the Weather App! ☀️🌧️</div>", unsafe_allow_html=True)
st.title("☁️ Live Weather Dashboard")

cities = st.multiselect("Select Cities:", list(weather_data.keys()), default=["Karachi"])

if st.button("Get Weather"):
    for city in cities:
        data = weather_data.get(city)
        
        if data:
            st.subheader(f"🌆 Weather in {city}")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🌡️ Temperature", f"{data['temp']}°C")
            with col2:
                st.metric("💧 Humidity", f"{data['humidity']}%")
            with col3:
                st.metric("💨 Wind Speed", f"{data['wind']} m/s")
            with col4:
                st.metric("🌍 Pressure", f"{data['pressure']} hPa")
            
            # Data Visualization
            df = pd.DataFrame({
                "Weather Metrics": ["Temperature", "Humidity", "Wind Speed", "Pressure"],
                "Values": [data['temp'], data['humidity'], data['wind'], data['pressure']]
            })
            fig = px.bar(df, x="Weather Metrics", y="Values", color="Weather Metrics", title=f"📊 Weather Data for {city}", text_auto=True, template="plotly_dark" if theme == "Dark" else "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"🔍 City {city} not found! Showing some approximate weather data.")
            approx_data = {"temp": 25, "humidity": 60, "wind": 9, "pressure": 1013}
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🌡️ Temperature", f"{approx_data['temp']}°C")
            with col2:
                st.metric("💧 Humidity", f"{approx_data['humidity']}%")
            with col3:
                st.metric("💨 Wind Speed", f"{approx_data['wind']} m/s")
            with col4:
                st.metric("🌍 Pressure", f"{approx_data['pressure']} hPa")
