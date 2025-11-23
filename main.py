"""Main entry point for the Weather Calendar Agent."""
import schedule
import time
from calendar_agent import WeatherCalendarAgent
from config import Config


def get_location():
    """Prompt user for location."""
    # Try to get location from env first, otherwise prompt
    default_location = Config.WEATHER_LOCATION if Config.WEATHER_LOCATION != 'New York,US' else None
    
    if default_location:
        print(f"Default location from config: {default_location}")
        use_default = input(f"Use this location? (Y/n): ").strip().lower()
        if use_default != 'n':
            return default_location
    
    print("\nEnter the location for weather forecasts.")
    print("Format: City,CountryCode (e.g., 'San Francisco,US' or 'London,GB')")
    location = input("Location: ").strip()
    
    if not location:
        print("No location provided. Using default: New York,US")
        return "New York,US"
    
    return location


def get_units():
    """Prompt user for units preference."""
    default_units = Config.WEATHER_UNITS
    
    print(f"\nSelect temperature and wind speed units:")
    print(f"1. Imperial (Fahrenheit, mph)")
    print(f"2. Metric (Celsius, m/s)")
    
    if default_units == 'imperial':
        print(f"Default: Imperial (press Enter to use default)")
        choice = input("Choice (1/2): ").strip()
        if not choice:
            return 'imperial'
    else:
        print(f"Default: Metric (press Enter to use default)")
        choice = input("Choice (1/2): ").strip()
        if not choice:
            return 'metric'
    
    if choice == '1':
        return 'imperial'
    elif choice == '2':
        return 'metric'
    else:
        print(f"Invalid choice. Using default: {default_units}")
        return default_units


def main():
    """Main function to run the weather calendar agent."""
    print("="*60)
    print("Weather Calendar Agent - Starting...")
    print("="*60)
    
    location = get_location()
    units = get_units()
    
    print(f"\nCalendar: {Config.CALENDAR_NAME}")
    print(f"Location: {location}")
    print(f"Units: {units.capitalize()}")
    print(f"Check Interval: Every 1 minute")
    print(f"Forecast Days: {Config.FORECAST_DAYS}")
    print("="*60)
    
    agent = WeatherCalendarAgent(location=location, units=units)
    
    # Run immediately on startup
    print("\nRunning initial sync...")
    agent.run_once()
    
    # Schedule periodic updates - every minute
    schedule.every(1).minutes.do(agent.run_once)
    
    print(f"\nScheduled to run every 1 minute.")
    print("Press Ctrl+C to stop.\n")
    
    # Keep the script running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\nShutting down Weather Calendar Agent...")
        print("Goodbye!")


if __name__ == "__main__":
    main()


