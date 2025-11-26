# Quick Installation Guide

## Step 1: Create Extension Icon

You need one icon file. You can:
- Use any image editor to create a 128x128 pixel PNG file
- Or use an online tool like [Favicon Generator](https://www.favicon-generator.org/)
- Place it in the `icons` folder as:
  - `icon.png`

## Step 2: Configure Google OAuth for Chrome Extension

**Important**: You need to create a new OAuth 2.0 Client ID specifically for Chrome extensions.

1. **Load the extension first to get your Extension ID:**
   - Open `chrome://extensions/`
   - Enable Developer mode
   - Click "Load unpacked" and select the `extension` folder
   - Copy the Extension ID shown on the extension card (looks like: `abcdefghijklmnopqrstuvwxyz123456`)

2. **Create OAuth Client in Google Cloud Console:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Select your project
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - **Application type**: Select "Chrome App" (NOT Desktop app or Web application)
   - **Application ID**: Enter your Extension ID (from step 1)
   - Click "Create"
   - **Copy the Client ID** that's generated

3. **Update `manifest.json`:**
   - Open `extension/manifest.json`
   - Replace the `client_id` in the `oauth2` section (line 16) with the Client ID you just copied
   - Save the file

4. **Reload the extension:**
   - Go back to `chrome://extensions/`
   - Click the refresh icon on your extension card
   - Try authorizing again

## Step 3: Load and Use

1. The extension should already be loaded (from Step 2)
2. Click the extension icon
3. Click "Authorize Google Calendar"
4. Enter your location and OpenWeatherMap API key
5. Click "Save Settings"
6. The extension will automatically sync every 15 minutes!

## Troubleshooting

- **Icons missing**: The extension will work but show default icons. Create the PNG file to fix this.
- **"bad client id" error**: 
  - Make sure you created an OAuth client with type "Chrome App" (NOT Desktop app)
  - Make sure the Application ID matches your Extension ID exactly
  - Make sure you updated the client_id in manifest.json and reloaded the extension
- **Auth not working**: 
  - Verify the Client ID in manifest.json matches the one in Google Cloud Console
  - Make sure you selected "Chrome App" as the application type
  - Try removing and re-adding the extension
- **No updates**: Check that settings are saved and you've authorized Google Calendar

