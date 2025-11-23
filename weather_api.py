"""Weather API integration for fetching forecasts."""
import requests
from datetime import datetime, timedelta
from config import Config


class WeatherAPI:
    """Handles weather data fetching from OpenWeatherMap API."""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    # Mapping of common province/state codes to country codes
    PROVINCE_TO_COUNTRY = {
        # Canadian provinces
        'ON': 'CA', 'QC': 'CA', 'BC': 'CA', 'AB': 'CA', 'MB': 'CA',
        'SK': 'CA', 'NS': 'CA', 'NB': 'CA', 'NL': 'CA', 'PE': 'CA',
        'NT': 'CA', 'YT': 'CA', 'NU': 'CA',
        # US states (common ones)
        'NY': 'US', 'CA': 'US', 'TX': 'US', 'FL': 'US', 'IL': 'US',
        'PA': 'US', 'OH': 'US', 'GA': 'US', 'NC': 'US', 'MI': 'US',
    }
    
    def __init__(self, location=None, units=None):
        self.api_key = Config.WEATHER_API_KEY
        raw_location = location or Config.WEATHER_LOCATION
        self.location = self._normalize_location(raw_location)
        self.units = units or Config.WEATHER_UNITS
        
        if not self.api_key:
            raise ValueError("WEATHER_API_KEY not set in environment variables")
        
        if not self.location:
            raise ValueError("Location must be provided")
        
        if self.units not in ['imperial', 'metric']:
            raise ValueError("Units must be 'imperial' or 'metric'")
    
    def _normalize_location(self, location):
        """Normalize location format, converting province codes to country codes."""
        if not location:
            return location
        
        # Check if location has a comma (city,code format)
        if ',' in location:
            parts = location.split(',')
            if len(parts) == 2:
                city = parts[0].strip()
                code = parts[1].strip().upper()
                
                # If it's a province code, convert to country code
                if code in self.PROVINCE_TO_COUNTRY:
                    country_code = self.PROVINCE_TO_COUNTRY[code]
                    return f"{city},{country_code}"
        
        return location
    
    def get_current_weather(self):
        """Get current weather conditions."""
        url = f"{self.BASE_URL}/weather"
        params = {
            'q': self.location,
            'appid': self.api_key,
            'units': self.units
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Error: Location '{self.location}' not found.")
                print(f"Please check the location format. Use 'City,CountryCode' (e.g., 'Toronto,CA' or 'New York,US')")
            else:
                print(f"Error fetching current weather: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching current weather: {e}")
            return None
    
    def get_forecast(self, days=5):
        """Get weather forecast for the next N days."""
        url = f"{self.BASE_URL}/forecast"
        params = {
            'q': self.location,
            'appid': self.api_key,
            'units': self.units,
            'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Group forecasts by day
            daily_forecasts = {}
            for item in data.get('list', []):
                dt = datetime.fromtimestamp(item['dt'])
                date_key = dt.date()
                
                if date_key not in daily_forecasts:
                    daily_forecasts[date_key] = []
                
                daily_forecasts[date_key].append({
                    'datetime': dt,
                    'temp': item['main']['temp'],
                    'feels_like': item['main']['feels_like'],
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'weather': item['weather'][0],
                    'wind_speed': item.get('wind', {}).get('speed', 0),
                    'wind_gust': item.get('wind', {}).get('gust', 0),
                    'wind_deg': item.get('wind', {}).get('deg', 0),
                    'rain': item.get('rain', {}).get('3h', 0),
                    'snow': item.get('snow', {}).get('3h', 0),
                    'clouds': item.get('clouds', {}).get('all', 0),
                    'visibility': item.get('visibility', 0),
                })
            
            return daily_forecasts
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"Error: Location '{self.location}' not found.")
                print(f"Please check the location format. Use 'City,CountryCode' (e.g., 'Toronto,CA' or 'New York,US')")
                print(f"Note: Canadian cities should use 'CA' (e.g., 'Toronto,CA'), not province codes like 'ON'")
            else:
                print(f"Error fetching forecast: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching forecast: {e}")
            return None
    
    def get_uv_index(self, lat=None, lon=None):
        """Get UV index forecast (requires lat/lon)."""
        # First get coordinates if not provided
        if lat is None or lon is None:
            current = self.get_current_weather()
            if current:
                lat = current['coord']['lat']
                lon = current['coord']['lon']
            else:
                return None
        
        url = f"https://api.openweathermap.org/data/2.5/uvi/forecast"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching UV index: {e}")
            return None
    
    def get_daily_summary(self, date):
        """Get a summary of weather conditions for a specific date."""
        forecasts = self.get_forecast(Config.FORECAST_DAYS)
        if not forecasts or date not in forecasts:
            return None
        
        day_forecasts = forecasts[date]
        if not day_forecasts:
            return None
        
        # Calculate daily aggregates
        temps = [f['temp'] for f in day_forecasts]
        feels_like = [f['feels_like'] for f in day_forecasts]
        rain_total = sum(f['rain'] for f in day_forecasts)
        snow_total = sum(f['snow'] for f in day_forecasts)
        wind_speeds = [f['wind_speed'] for f in day_forecasts]
        wind_gusts = [f['wind_gust'] for f in day_forecasts if f['wind_gust']]
        
        return {
            'date': date,
            'temp_min': min(temps),
            'temp_max': max(temps),
            'temp_avg': sum(temps) / len(temps),
            'feels_like_min': min(feels_like),
            'feels_like_max': max(feels_like),
            'rain_total': rain_total,
            'snow_total': snow_total,
            'wind_max': max(wind_speeds) if wind_speeds else 0,
            'wind_gust_max': max(wind_gusts) if wind_gusts else 0,
            'conditions': day_forecasts[0]['weather']['main'],
            'description': day_forecasts[0]['weather']['description'],
            'humidity_avg': sum(f['humidity'] for f in day_forecasts) / len(day_forecasts),
        }


