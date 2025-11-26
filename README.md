# Weather Calendar Agent

A backend service that automatically manages a Google Calendar called "Weather Alerts & Suggestions" by creating, updating, and deleting events based on weather forecasts.

## Features

- 🌧️ **Rain Alerts**: Creates events when significant rainfall is expected
- ❄️ **Snow Alerts**: Alerts for snowfall conditions
- 🌡️ **Temperature Alerts**: Warns about extreme cold or heat
- 💨 **Wind Alerts**: Notifies about high wind conditions
- ☀️ **UV Alerts**: Reminds about sun protection on clear days
- 🌤️ **Nice Weather Suggestions**: Highlights perfect weather days for outdoor activities

## Prerequisites

1. **Python 3.8+**
2. **Google Cloud Project** with Calendar API enabled
3. **OpenWeatherMap API Key** (free tier available)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Calendar API Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Calendar API**
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
5. Choose "Desktop app" as the application type
6. Download the credentials JSON file and save it as `credentials.json` in the project root
7. The first time you run the script, it will open a browser for authentication

### 3. OpenWeatherMap API Setup

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api) (free tier available)
2. Get your API key from the dashboard
3. Add it to your `.env` file (see Configuration below)

### 4. Configuration

Create a `.env` file in the project root:

```env
# Google Calendar API Configuration
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:8080/callback

# Weather API Configuration
WEATHER_API_KEY=your_openweathermap_api_key_here
WEATHER_LOCATION=New York,US
WEATHER_UNITS=imperial

# Calendar Configuration
CALENDAR_NAME=Weather Alerts & Suggestions

# Weather Thresholds
MIN_TEMPERATURE=32
MAX_TEMPERATURE=90
RAIN_THRESHOLD_MM=5.0
SNOW_THRESHOLD_MM=2.0
WIND_SPEED_THRESHOLD_MPH=25
UV_INDEX_THRESHOLD=6

# Service Configuration
CHECK_INTERVAL_HOURS=6
FORECAST_DAYS=5
```

### Configuration Options

- **WEATHER_LOCATION**: City name and country code (e.g., "New York,US", "London,GB")
- **WEATHER_UNITS**: "imperial" (Fahrenheit, mph) or "metric" (Celsius, m/s)
- **MIN_TEMPERATURE**: Temperature below which cold alerts are triggered
- **MAX_TEMPERATURE**: Temperature above which heat alerts are triggered
- **RAIN_THRESHOLD_MM**: Minimum rainfall (mm) to trigger rain alert
- **SNOW_THRESHOLD_MM**: Minimum snowfall (mm) to trigger snow alert
- **WIND_SPEED_THRESHOLD_MPH**: Wind speed threshold for wind alerts
- **CHECK_INTERVAL_HOURS**: How often to check and update the calendar
- **FORECAST_DAYS**: Number of days ahead to create events for

## Usage

### Option 1: Interactive Run (Continuous)

```bash
python main.py
```

The script will:
1. Prompt for location and units
2. Authenticate with Google Calendar (first time only)
3. Create the "Weather Alerts & Suggestions" calendar if it doesn't exist
4. Analyze the weather forecast
5. Create/update/delete calendar events accordingly
6. Continue running and update every minute

### Option 2: Scheduled Run (Recommended - No Continuous Process)

Use the scheduled run script with cron (Linux/Mac) or Task Scheduler (Windows) to run periodically without keeping your computer on.

#### For Linux/Mac (cron):

1. Edit your crontab:
   ```bash
   crontab -e
   ```

2. Add a line to run every hour (or adjust as needed):
   ```bash
   0 * * * * cd /path/to/The-Weather-Calendar && /usr/bin/python3 scheduled_run.py --location "Toronto,CA" --units metric >> /tmp/weather_calendar.log 2>&1
   ```

   Or every 6 hours:
   ```bash
   0 */6 * * * cd /path/to/The-Weather-Calendar && /usr/bin/python3 scheduled_run.py --location "Toronto,CA" --units metric >> /tmp/weather_calendar.log 2>&1
   ```

#### For Windows (Task Scheduler):

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (e.g., Daily, repeat every 6 hours)
4. Action: Start a program
   - Program: `python`
   - Arguments: `scheduled_run.py --location "Toronto,CA" --units metric`
   - Start in: `C:\path\to\The-Weather-Calendar`

#### Command-line usage:

```bash
python scheduled_run.py --location "Toronto,CA" --units metric
```

### Option 3: Cloud Deployment

Deploy to a cloud service that runs on a schedule:

- **AWS Lambda** with EventBridge (CloudWatch Events)
- **Google Cloud Functions** with Cloud Scheduler
- **Azure Functions** with Timer Trigger
- **Heroku Scheduler** (free tier available)
- **PythonAnywhere** scheduled tasks

Example for Heroku Scheduler:
1. Deploy to Heroku
2. Add Heroku Scheduler addon
3. Set command: `python scheduled_run.py --location "Toronto,CA" --units metric`
4. Set frequency (e.g., every 6 hours)

### Option 4: Run as a Background Service

For production use, consider running as a systemd service (Linux) or using a process manager like `supervisord` or `pm2`.

Example systemd service file:

```ini
[Unit]
Description=Weather Calendar Agent
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/The-Weather-Calendar
ExecStart=/usr/bin/python3 /path/to/The-Weather-Calendar/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## How It Works

1. **Weather Analysis**: Fetches weather forecast from OpenWeatherMap API
2. **Event Generation**: Analyzes forecast data and generates event suggestions based on configured thresholds
3. **Calendar Sync**: 
   - Creates new events for new weather conditions
   - Updates existing events if conditions change
   - Deletes events that are no longer relevant
4. **Scheduling**: Runs periodically to keep the calendar up-to-date

## Event Types

- **Cold Weather Alert**: When temperatures drop below threshold
- **Heat Alert**: When temperatures exceed threshold
- **Rain Expected**: Significant rainfall forecast
- **Snow Expected**: Snowfall forecast
- **High Winds**: Strong wind conditions
- **High UV Expected**: Clear/sunny days requiring sun protection
- **Perfect Weather Day**: Ideal conditions for outdoor activities

## Troubleshooting

### Authentication Issues

- Ensure `credentials.json` is in the project root
- Delete `token.pickle` and re-authenticate if token expires
- Check that Calendar API is enabled in Google Cloud Console

### Weather API Issues

- Verify your OpenWeatherMap API key is valid
- Check that the location format is correct (e.g., "City,CountryCode")
- Ensure you haven't exceeded API rate limits

### Calendar Not Found

- The script automatically creates the calendar if it doesn't exist
- Check that you have calendar creation permissions in your Google account

## License

MIT License - feel free to use and modify as needed.


