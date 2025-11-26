# Permission Justifications for Chrome Web Store

## Identity Justification

**Required for:** Google Calendar OAuth authentication

The identity permission is essential for authenticating with Google Calendar API using Chrome's secure OAuth 2.0 flow. This allows the extension to create, update, and delete weather events in the user's Google Calendar. Without this permission, the extension cannot access the user's calendar to sync weather alerts. The authentication is handled entirely through Chrome's secure identity API, ensuring user credentials are never exposed to the extension code.

## Storage Justification

**Required for:** Local preference storage

The storage permission is used to save user preferences locally in Chrome's storage API. This includes the user's location, OpenWeatherMap API key, unit preferences (Imperial/Metric), and last sync timestamp. All data is stored locally on the user's device and never transmitted to external servers. This permission is necessary to remember user settings between browser sessions and provide a seamless user experience without requiring reconfiguration each time.

## Alarms Justification

**Required for:** Scheduled automatic weather updates

The alarms permission is used to schedule automatic weather forecast updates every 15 minutes in the background. This ensures the user's calendar stays current with the latest weather information without requiring manual intervention. The extension uses Chrome's alarms API to create a recurring alarm that triggers the weather sync process, keeping calendar events up-to-date with changing weather conditions.

## Host Permission Justification

**Required for:** API access to Google Calendar and OpenWeatherMap

The extension requires host permissions for two external APIs:

1. **https://www.googleapis.com/*** - This permission is required to access Google Calendar API endpoints. The extension needs to:
   - List and create calendars
   - Create, update, and delete calendar events
   - Authenticate using OAuth tokens
   Without this permission, the extension cannot sync weather events to the user's Google Calendar.

2. **https://api.openweathermap.org/*** - This permission is required to fetch weather forecast data from OpenWeatherMap API. The extension uses the user's API key to retrieve weather forecasts for their specified location. This is the core functionality that enables the extension to generate weather alerts and suggestions.

Both API endpoints are necessary for the extension's single purpose: automatically syncing weather information to Google Calendar.

## Remote Code Justification

**Answer: No, I am not using remote code**

The extension does not use remote code. All JavaScript code is included in the extension package:
- background.js (service worker)
- popup.js (popup script)
- All code is bundled in the extension ZIP file
- No external script tags or dynamic code evaluation
- No references to external JavaScript files
- All API calls are direct fetch requests to documented APIs, not code execution

