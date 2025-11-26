# Weather Calendar Agent - Chrome Extension

A Chrome extension that automatically manages a Google Calendar with weather alerts and suggestions, updating every 15 minutes.

## Features

- 🌧️ **Rain Alerts**: Creates events when significant rainfall is expected
- ❄️ **Snow Alerts**: Alerts for snowfall conditions
- 🌡️ **Temperature Alerts**: Warns about extreme cold or heat
- 💨 **Wind Alerts**: Notifies about high wind conditions
- ☀️ **UV Alerts**: Reminds about sun protection on clear days
- 🌤️ **Nice Weather Suggestions**: Highlights perfect weather days for outdoor activities

## Installation

### 1. Set Up Google OAuth for Chrome Extension

**Important**: You must create a new OAuth 2.0 Client ID with type "Chrome App" (NOT Desktop app):

1. Load the extension first to get your Extension ID:
   - Open `chrome://extensions/`
   - Enable Developer mode
   - Click "Load unpacked" and select the `extension` folder
   - Copy the Extension ID shown on the extension card

2. Create OAuth Client in Google Cloud Console:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Select your project
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - **Application type**: Select "Chrome App" (this is different from Desktop app!)
   - **Application ID**: Enter your Extension ID from step 1
   - Click "Create"
   - Copy the Client ID that's generated

3. Update `manifest.json`:
   - Open `extension/manifest.json`
   - Replace the `client_id` in the `oauth2` section with the Client ID you just copied
   - Save the file
   - Reload the extension in `chrome://extensions/`

### 2. Create Extension Icon

Create an icon file in the `icons` folder:
- `icon.png` (128x128 pixels recommended)

You can use any image editor or online tool to create a weather-themed icon.

### 3. Load the Extension

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `extension` folder from this project
5. Copy your Extension ID from the extension card
6. Update the OAuth redirect URI in Google Cloud Console with your Extension ID

### 4. Configure Settings

1. Click the extension icon in your toolbar
2. Click "Authorize Google Calendar" and sign in
3. Enter your location (e.g., "Toronto,CA" or "New York,US")
4. Enter your OpenWeatherMap API key
5. Select your preferred units (Imperial or Metric)
6. Click "Save Settings"

### 3. Get OpenWeatherMap API Key

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api) (free tier available)
2. Get your API key from the dashboard
3. Enter it in the extension popup

## How It Works

- The extension runs in the background and automatically syncs weather events every 15 minutes
- It creates a calendar called "Weather Alerts & Suggestions" in your Google Calendar
- Events are automatically created, updated, and deleted based on the weather forecast
- You can manually trigger a sync by clicking "Sync Now" in the popup

## Permissions

The extension requires:
- **Identity**: To authenticate with Google Calendar API
- **Storage**: To save your settings
- **Alarms**: To schedule automatic updates every 15 minutes
- **Host permissions**: To access Google Calendar API and OpenWeatherMap API

## Troubleshooting

### Authorization Issues

- **"bad client id" error**: 
  - You must create an OAuth client with type "Chrome App" (NOT Desktop app or Web application)
  - The Application ID must match your Extension ID exactly
  - Make sure you updated manifest.json and reloaded the extension
- Make sure you click "Authorize Google Calendar" and complete the sign-in process
- If authorization fails, try clicking "Re-authorize"
- Verify the Client ID in manifest.json matches the one in Google Cloud Console

### Weather Not Updating

- Check that your OpenWeatherMap API key is correct
- Verify your location format (City,CountryCode)
- Check the browser console for errors (chrome://extensions → Details → Inspect views: service worker)

### Events Not Appearing

- Make sure the calendar "Weather Alerts & Suggestions" exists in your Google Calendar
- Check that you've authorized the extension
- Try clicking "Sync Now" manually

## Development

To modify the extension:

1. Make changes to the files in the `extension` folder
2. Go to `chrome://extensions/`
3. Click the refresh icon on the extension card
4. Test your changes

## Notes

- The extension updates every 15 minutes automatically
- You can manually sync at any time using the "Sync Now" button
- Settings are stored locally in Chrome storage
- The extension uses Chrome's identity API for OAuth authentication

