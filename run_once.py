"""Run a single sync operation without scheduling."""
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

if __name__ == "__main__":
    print("="*60)
    print("Weather Calendar Agent - Single Run")
    print("="*60)
    
    location = get_location()
    units = get_units()
    
    print(f"\nUsing location: {location}")
    print(f"Using units: {units.capitalize()}\n")
    agent = WeatherCalendarAgent(location=location, units=units)
    agent.run_once()


