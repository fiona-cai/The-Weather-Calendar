"""Configuration management for the Weather Calendar Agent."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Google Calendar API
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
    GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8080/callback')
    CALENDAR_NAME = os.getenv('CALENDAR_NAME', 'Weather Alerts & Suggestions')
    
    # Weather API
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', '')
    WEATHER_LOCATION = os.getenv('WEATHER_LOCATION', 'New York,US')
    WEATHER_UNITS = os.getenv('WEATHER_UNITS', 'imperial')
    
    # Weather Thresholds
    MIN_TEMPERATURE = float(os.getenv('MIN_TEMPERATURE', '32'))
    MAX_TEMPERATURE = float(os.getenv('MAX_TEMPERATURE', '90'))
    RAIN_THRESHOLD_MM = float(os.getenv('RAIN_THRESHOLD_MM', '5.0'))
    SNOW_THRESHOLD_MM = float(os.getenv('SNOW_THRESHOLD_MM', '2.0'))
    WIND_SPEED_THRESHOLD_MPH = float(os.getenv('WIND_SPEED_THRESHOLD_MPH', '25'))
    UV_INDEX_THRESHOLD = float(os.getenv('UV_INDEX_THRESHOLD', '6'))
    
    # Service Configuration
    CHECK_INTERVAL_HOURS = int(os.getenv('CHECK_INTERVAL_HOURS', '6'))
    FORECAST_DAYS = int(os.getenv('FORECAST_DAYS', '5'))




