"""Test script that accepts command line arguments for non-interactive testing."""
import sys
from calendar_agent import WeatherCalendarAgent

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python test_run.py <location> <units>")
        print("Example: python test_run.py 'San Francisco,US' imperial")
        print("Units: 'imperial' or 'metric'")
        sys.exit(1)
    
    location = sys.argv[1]
    units = sys.argv[2]
    
    if units not in ['imperial', 'metric']:
        print("Error: Units must be 'imperial' or 'metric'")
        sys.exit(1)
    
    print(f"Running with location: {location}, units: {units}")
    agent = WeatherCalendarAgent(location=location, units=units)
    agent.run_once()

