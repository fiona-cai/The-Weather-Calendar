# Privacy Policy for Weather Calendar Agent

**Last Updated:** [Current Date]

## Introduction

Weather Calendar Agent ("we", "our", or "the extension") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, and safeguard your information when you use our Chrome extension.

## Information We Collect

### Data Stored Locally
The extension stores the following information locally on your device using Chrome's storage API:
- Your location preference (city and country code)
- Your OpenWeatherMap API key
- Your unit preference (Imperial or Metric)
- Last sync timestamp
- Google Calendar authentication token (managed by Chrome)

### Data We Do NOT Collect
- We do not collect any personal information
- We do not track your browsing activity
- We do not share your data with third parties
- We do not use analytics or tracking services
- We do not store your data on external servers

## How We Use Your Information

### Local Storage
All information is stored locally in your Chrome browser and is only used to:
- Remember your location and preferences
- Authenticate with Google Calendar API
- Fetch weather data from OpenWeatherMap API

### Third-Party Services

**Google Calendar API:**
- We use Google's OAuth 2.0 for authentication
- We only request calendar write permissions to create/update/delete weather events
- Your Google account credentials are never stored by us
- Authentication is handled entirely by Chrome's identity API

**OpenWeatherMap API:**
- We use your API key to fetch weather forecasts
- API requests are made directly from your browser to OpenWeatherMap
- We do not intercept or store weather data

## Data Security

- All data is stored locally in Chrome's secure storage
- OAuth authentication is handled by Chrome's secure identity API
- No data is transmitted to our servers (we don't have any)
- Your OpenWeatherMap API key is stored locally and only used for API requests

## Permissions Explained

**Identity Permission:**
- Used to authenticate with Google Calendar API
- Required to create and manage calendar events
- Managed entirely by Chrome's secure OAuth flow

**Storage Permission:**
- Used to save your preferences locally
- All data remains on your device

**Alarms Permission:**
- Used to schedule automatic weather updates every 15 minutes
- Runs entirely in the background

**Host Permissions:**
- `https://www.googleapis.com/*` - Required for Google Calendar API
- `https://api.openweathermap.org/*` - Required for weather data

## Your Rights

- You can revoke Google Calendar access at any time through your Google Account settings
- You can delete all stored data by uninstalling the extension
- You can view your stored data through Chrome's developer tools

## Changes to This Policy

We may update this Privacy Policy from time to time. We will notify you of any changes by updating the "Last Updated" date.

## Contact

For questions about this Privacy Policy, please contact us through the extension's support channel.

## Open Source

This extension is open source. You can review the code to verify our privacy practices.

