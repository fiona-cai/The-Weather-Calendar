"""Main calendar agent that orchestrates weather monitoring and calendar updates."""
from datetime import datetime, timedelta
from google_calendar import GoogleCalendarManager
from weather_analyzer import WeatherAnalyzer
from config import Config


class WeatherCalendarAgent:
    """Main agent that manages weather-based calendar events."""
    
    def __init__(self, location=None, units=None):
        self.calendar_manager = GoogleCalendarManager()
        self.weather_analyzer = WeatherAnalyzer(location=location, units=units)
        self.location = location
        self.units = units
        self.event_mapping = {}  # Maps event keys to calendar event IDs
    
    def sync_weather_events(self):
        """Sync weather events with the calendar."""
        print(f"\n{'='*60}")
        print(f"Weather Calendar Sync - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Get suggested events from weather analysis
        suggested_events = self.weather_analyzer.analyze_forecast(Config.FORECAST_DAYS)
        
        # Get existing events from calendar
        time_min = datetime.now()
        time_max = time_min + timedelta(days=Config.FORECAST_DAYS)
        existing_events = self.calendar_manager.list_events(time_min, time_max)
        
        # Create a mapping of existing events by their title pattern
        existing_by_key = {}
        for event in existing_events:
            # Try to match events by title patterns
            title = event.get('summary', '')
            start_str = event.get('start', {}).get('dateTime', '')
            if start_str:
                try:
                    start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                    event_key = self._extract_event_key(title, start_dt.date())
                    if event_key:
                        existing_by_key[event_key] = event
                except:
                    pass
        
        # Process suggested events
        current_event_keys = set()
        
        for event in suggested_events:
            event_key = self.weather_analyzer.get_event_key(event)
            current_event_keys.add(event_key)
            
            if event_key in existing_by_key:
                # Event exists, check if update needed
                existing_event = existing_by_key[event_key]
                if self.weather_analyzer.should_update_event(existing_event, event):
                    self.calendar_manager.update_event(
                        existing_event['id'],
                        event['title'],
                        event['description'],
                        event['start_time'],
                        event['end_time']
                    )
                    print(f"✓ Updated: {event['title']}")
                else:
                    print(f"- No update needed: {event['title']}")
            else:
                # New event, create it
                event_id = self.calendar_manager.create_event(
                    event['title'],
                    event['description'],
                    event['start_time'],
                    event['end_time']
                )
                if event_id:
                    self.event_mapping[event_key] = event_id
                    print(f"✓ Created: {event['title']}")
        
        # Remove events that are no longer relevant
        for event_key, existing_event in existing_by_key.items():
            if event_key not in current_event_keys:
                # Check if event is in the future and should be removed
                start_str = existing_event.get('start', {}).get('dateTime', '')
                if start_str:
                    try:
                        start_dt = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                        if start_dt > datetime.now():
                            self.calendar_manager.delete_event(existing_event['id'])
                            print(f"✓ Deleted outdated: {existing_event.get('summary', 'Unknown')}")
                    except:
                        pass
        
        print(f"\n{'='*60}")
        print(f"Sync complete! Processed {len(suggested_events)} weather events.")
        print(f"{'='*60}\n")
    
    def _extract_event_key(self, title, date):
        """Extract event key from title and date."""
        # Simple pattern matching - look for event type indicators
        if 'Cold Weather Alert' in title or '❄️ Cold Weather' in title:
            return f"cold_alert_{date}"
        elif 'Heat Alert' in title or '🔥 Heat Alert' in title:
            return f"heat_alert_{date}"
        elif 'Rain Expected' in title or '🌧️ Rain' in title:
            return f"rain_alert_{date}"
        elif 'Snow Expected' in title or '❄️ Snow' in title:
            return f"snow_alert_{date}"
        elif 'High Winds' in title or '💨 High Winds' in title:
            return f"wind_alert_{date}"
        elif 'High UV' in title or '☀️ High UV' in title:
            return f"uv_alert_{date}"
        elif 'Perfect Weather' in title or '☀️ Perfect Weather' in title:
            return f"nice_weather_{date}"
        return None
    
    def run_once(self):
        """Run a single sync operation."""
        try:
            self.sync_weather_events()
        except Exception as e:
            print(f"Error during sync: {e}")
            import traceback
            traceback.print_exception(type(e), e, e.__traceback__)


