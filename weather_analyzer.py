"""Analyzes weather data and generates calendar event suggestions."""
from datetime import datetime, timedelta, time
from config import Config
from weather_api import WeatherAPI


class WeatherAnalyzer:
    """Analyzes weather forecasts and determines what events to create."""
    
    def __init__(self, location=None, units=None):
        self.weather_api = WeatherAPI(location=location, units=units)
        self.config = Config
        self.units = units or Config.WEATHER_UNITS
    
    def analyze_forecast(self, days_ahead=5):
        """Analyze weather forecast and return list of suggested events."""
        events = []
        forecasts = self.weather_api.get_forecast(days_ahead)
        
        if not forecasts:
            return events
        
        for date, day_forecasts in forecasts.items():
            if not day_forecasts:
                continue
            
            # Get daily summary
            summary = self.weather_api.get_daily_summary(date)
            if not summary:
                continue
            
            # Analyze different weather conditions
            date_events = []
            
            # Get unit symbols
            temp_unit = '°F' if self.units == 'imperial' else '°C'
            wind_unit = 'mph' if self.units == 'imperial' else 'm/s'
            
            # Convert temperature thresholds based on units
            # Config defaults are in Fahrenheit
            min_temp = self.config.MIN_TEMPERATURE
            max_temp = self.config.MAX_TEMPERATURE
            if self.units == 'metric':
                # Convert Fahrenheit to Celsius: C = (F - 32) * 5/9
                min_temp = (min_temp - 32) * 5 / 9
                max_temp = (max_temp - 32) * 5 / 9
            
            # Temperature alerts
            if summary['temp_min'] < min_temp:
                date_events.append({
                    'type': 'cold_alert',
                    'title': f'❄️ Cold Weather Alert - {summary["temp_min"]:.0f}{temp_unit}',
                    'description': f'Very cold temperatures expected. Low: {summary["temp_min"]:.0f}{temp_unit}, High: {summary["temp_max"]:.0f}{temp_unit}. Dress warmly!',
                    'start_time': datetime.combine(date, time(7, 0)),
                    'end_time': datetime.combine(date, time(9, 0)),
                })
            
            if summary['temp_max'] > max_temp:
                date_events.append({
                    'type': 'heat_alert',
                    'title': f'🔥 Heat Alert - {summary["temp_max"]:.0f}{temp_unit}',
                    'description': f'Hot temperatures expected. High: {summary["temp_max"]:.0f}{temp_unit}, Low: {summary["temp_min"]:.0f}{temp_unit}. Stay hydrated and avoid prolonged sun exposure!',
                    'start_time': datetime.combine(date, time(10, 0)),
                    'end_time': datetime.combine(date, time(18, 0)),
                })
            
            # Rain alerts
            if summary['rain_total'] >= self.config.RAIN_THRESHOLD_MM:
                date_events.append({
                    'type': 'rain_alert',
                    'title': f'🌧️ Rain Expected - {summary["rain_total"]:.1f}mm',
                    'description': f'Significant rainfall expected ({summary["rain_total"]:.1f}mm). Remember to bring an umbrella and plan indoor activities.',
                    'start_time': datetime.combine(date, time(6, 0)),
                    'end_time': datetime.combine(date, time(22, 0)),
                })
            
            # Snow alerts
            if summary['snow_total'] >= self.config.SNOW_THRESHOLD_MM:
                date_events.append({
                    'type': 'snow_alert',
                    'title': f'❄️ Snow Expected - {summary["snow_total"]:.1f}mm',
                    'description': f'Snowfall expected ({summary["snow_total"]:.1f}mm). Allow extra travel time and drive carefully.',
                    'start_time': datetime.combine(date, time(6, 0)),
                    'end_time': datetime.combine(date, time(22, 0)),
                })
            
            # Wind alerts - convert threshold if needed
            wind_threshold = self.config.WIND_SPEED_THRESHOLD_MPH
            if self.units == 'metric':
                # Convert mph to m/s (1 mph ≈ 0.447 m/s)
                wind_threshold = wind_threshold * 0.447
            
            if summary['wind_max'] >= wind_threshold:
                date_events.append({
                    'type': 'wind_alert',
                    'title': f'💨 High Winds - {summary["wind_max"]:.0f} {wind_unit}',
                    'description': f'Strong winds expected (up to {summary["wind_max"]:.0f} {wind_unit}, gusts up to {summary["wind_gust_max"]:.0f} {wind_unit}). Secure outdoor items and be cautious.',
                    'start_time': datetime.combine(date, time(8, 0)),
                    'end_time': datetime.combine(date, time(20, 0)),
                })
            
            # UV index (simplified - using clear sky conditions as proxy)
            # Note: OpenWeatherMap free tier doesn't include UV in forecast
            # This is a simplified check based on cloud cover
            if summary['conditions'] in ['Clear', 'Sunny'] and date >= datetime.now().date():
                date_events.append({
                    'type': 'uv_alert',
                    'title': f'☀️ High UV Expected',
                    'description': f'Clear/sunny conditions expected. Remember sunscreen and UV protection, especially between 10 AM - 4 PM.',
                    'start_time': datetime.combine(date, time(10, 0)),
                    'end_time': datetime.combine(date, time(16, 0)),
                })
            
            # Nice weather suggestions - adjust thresholds based on units
            nice_temp_min = 60 if self.units == 'imperial' else 15.5  # 60°F ≈ 15.5°C
            nice_temp_max = 80 if self.units == 'imperial' else 26.7  # 80°F ≈ 26.7°C
            nice_wind_max = 15 if self.units == 'imperial' else 6.7    # 15 mph ≈ 6.7 m/s
            
            if (summary['temp_min'] >= nice_temp_min and summary['temp_max'] <= nice_temp_max and 
                summary['rain_total'] < 1 and summary['wind_max'] < nice_wind_max and
                summary['conditions'] in ['Clear', 'Sunny', 'Partly Cloudy']):
                date_events.append({
                    'type': 'nice_weather',
                    'title': f'☀️ Perfect Weather Day!',
                    'description': f'Great weather expected! Temp: {summary["temp_min"]:.0f}{temp_unit} - {summary["temp_max"]:.0f}{temp_unit}, {summary["description"]}. Perfect for outdoor activities!',
                    'start_time': datetime.combine(date, time(9, 0)),
                    'end_time': datetime.combine(date, time(17, 0)),
                })
            
            events.extend(date_events)
        
        return events
    
    def get_event_key(self, event):
        """Generate a unique key for an event to track it."""
        return f"{event['type']}_{event['start_time'].date()}"
    
    def should_update_event(self, existing_event, new_event):
        """Determine if an existing event should be updated."""
        # Compare key fields to see if update is needed
        existing_title = existing_event.get('summary', '')
        new_title = new_event['title']
        
        existing_desc = existing_event.get('description', '')
        new_desc = new_event['description']
        
        # Update if title or description changed
        if existing_title != new_title or existing_desc != new_desc:
            return True
        
        return False


