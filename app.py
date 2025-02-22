import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Constants
API_KEY = "your_api_key"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_weather(city):
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_forecast(city, days=7):
    params = {"q": city, "appid": API_KEY, "units": "metric", "cnt": days * 8}  # 8 data points per day (3-hour intervals)
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Custom CSS & Theme Selection
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark", "Modern"])

st.markdown("""
    <style>
    .welcome-box { text-align: center; padding: 20px; font-size: 26px; font-weight: bold; background: linear-gradient(90deg, #ff8a00, #e52e71); color: white; border-radius: 10px; }
    .main-container { padding: 20px; border-radius: 12px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); }
    .metric-box { border-radius: 8px; padding: 10px; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

if theme == "Dark":
    st.markdown("""
        <style>
        body { background-color: #1e1e1e; color: white; }
        .main-container { background-color: #333; }
        .metric-box { background-color: #444; color: white; }
        </style>
    """, unsafe_allow_html=True)
elif theme == "Modern":
    st.markdown("""
        <style>
        body { background-color: #2b2b2b; color: #e0e0e0; }
        .main-container { background-color: #3c3c3c; }
        .metric-box { background-color: #4a4a4a; color: white; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .main-container { background-color: #f0f2f6; }
        .metric-box { background-color: white; }
        </style>
    """, unsafe_allow_html=True)

# Streamlit UI
st.set_page_config(page_title="Weather App", page_icon="☁️", layout="wide")
st.markdown("<div class='welcome-box'>🌎 Welcome to the Weather App! ☀️🌧️</div>", unsafe_allow_html=True)
st.title("☁️ Live Weather Dashboard")

cities = st.multiselect("Select Cities:", ["New York", "London", "Tokyo", "Mumbai", "Sydney"], default=["New York"])

days = st.slider("Select Forecast Duration (Days)", min_value=1, max_value=7, value=3)

if st.button("Get Weather"):
    for city in cities:
        data = get_weather(city)
        forecast_data = get_forecast(city, days)
        
        if data:
            st.subheader(f"🌆 Weather in {city}")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("🌡️ Temperature", f"{data['main']['temp']}°C")
            with col2:
                st.metric("💧 Humidity", f"{data['main']['humidity']}%")
            with col3:
                st.metric("💨 Wind Speed", f"{data['wind']['speed']} m/s")
            with col4:
                st.metric("🌍 Pressure", f"{data['main']['pressure']} hPa")
            
            # Weekly Forecast
            if forecast_data:
                times = [entry['dt_txt'] for entry in forecast_data['list']]
                temps = [entry['main']['temp'] for entry in forecast_data['list']]
                forecast_df = pd.DataFrame({"Time": times, "Temperature (°C)": temps})
                fig_forecast = px.line(forecast_df, x="Time", y="Temperature (°C)", title=f"📅 {days}-Day Temperature Forecast for {city}", markers=True, template="plotly_dark" if theme == "Dark" else "plotly_white")
                st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Data Visualization
            df = pd.DataFrame({
                "Weather Metrics": ["Temperature", "Humidity", "Wind Speed", "Pressure"],
                "Values": [data['main']['temp'], data['main']['humidity'], data['wind']['speed'], data['main']['pressure']]
            })
            fig = px.bar(df, x="Weather Metrics", y="Values", color="Weather Metrics", title=f"📊 Weather Data for {city}", text_auto=True, template="plotly_dark" if theme == "Dark" else "plotly_white")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"❌ City {city} not found! Please enter a valid city name.")
