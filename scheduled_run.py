"""Scheduled run script - runs once and exits. Use with cron or task scheduler."""
import sys
import argparse
from calendar_agent import WeatherCalendarAgent
from config import Config


def main():
    """Run a single sync operation with command-line arguments."""
    parser = argparse.ArgumentParser(description='Weather Calendar Agent - Scheduled Run')
    parser.add_argument('--location', type=str, required=True,
                        help='Location (e.g., "Toronto,CA" or "New York,US")')
    parser.add_argument('--units', type=str, choices=['imperial', 'metric'], 
                        default=Config.WEATHER_UNITS,
                        help='Units: imperial or metric (default: from config)')
    
    args = parser.parse_args()
    
    print(f"Weather Calendar Agent - Scheduled Run")
    print(f"Location: {args.location}")
    print(f"Units: {args.units}")
    print("="*60)
    
    try:
        agent = WeatherCalendarAgent(location=args.location, units=args.units)
        agent.run_once()
        print("Sync completed successfully!")
        sys.exit(0)
    except Exception as e:
        print(f"Error during sync: {e}")
        import traceback
        traceback.print_exception(type(e), e, e.__traceback__)
        sys.exit(1)


if __name__ == "__main__":
    main()



