// Background service worker for Weather Calendar Agent
const CALENDAR_NAME = 'Weather Alerts & Suggestions';
const UPDATE_INTERVAL_MINUTES = 15;

// Initialize on install
chrome.runtime.onInstalled.addListener(() => {
  console.log('Weather Calendar Agent installed');
  setupAlarm();
});

// Setup alarm for periodic updates
function setupAlarm() {
  chrome.alarms.create('weatherUpdate', {
    delayInMinutes: 1, // First run after 1 minute
    periodInMinutes: UPDATE_INTERVAL_MINUTES
  });
}

// Listen for alarm
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'weatherUpdate') {
    syncWeatherEvents();
  }
});

// Main sync function
async function syncWeatherEvents() {
  try {
    const settings = await getSettings();
    
    if (!settings.location || !settings.weatherApiKey) {
      console.log('Settings not configured yet');
      return;
    }

    console.log('Starting weather sync...');
    
    // Get weather forecast
    const forecasts = await getWeatherForecast(settings.location, settings.units, settings.weatherApiKey);
    if (!forecasts || Object.keys(forecasts).length === 0) {
      console.error('Failed to fetch weather forecast or no forecast data');
      return;
    }

    // Generate events
    const events = generateWeatherEvents(forecasts, settings);
    
    if (events.length === 0) {
      console.log('No weather events to sync');
      // Still update last sync time
      await chrome.storage.local.set({ lastSync: new Date().toISOString() });
      return;
    }
    
    // Get access token
    const token = await getAccessToken();
    if (!token) {
      console.error('Failed to get access token');
      return;
    }

    // Get or create calendar
    const calendarId = await getOrCreateCalendar(token);
    if (!calendarId) {
      console.error('Failed to get/create calendar');
      return;
    }

    // Sync events to calendar
    await syncEventsToCalendar(token, calendarId, events);
    
    console.log(`Weather sync completed successfully. Synced ${events.length} events.`);
    
    // Update last sync time
    await chrome.storage.local.set({ lastSync: new Date().toISOString() });
    
  } catch (error) {
    console.error('Error during weather sync:', error);
    // Don't throw - allow silent failure for background syncs
  }
}

// Get settings from storage
async function getSettings() {
  const result = await chrome.storage.local.get([
    'location',
    'units',
    'weatherApiKey',
    'minTemperature',
    'maxTemperature',
    'rainThreshold',
    'snowThreshold',
    'windThreshold'
  ]);
  
  return {
    location: result.location || '',
    units: result.units || 'imperial',
    weatherApiKey: result.weatherApiKey || '',
    minTemperature: result.minTemperature || (result.units === 'metric' ? 0 : 32),
    maxTemperature: result.maxTemperature || (result.units === 'metric' ? 32 : 90),
    rainThreshold: result.rainThreshold || 5.0,
    snowThreshold: result.snowThreshold || 2.0,
    windThreshold: result.windThreshold || (result.units === 'metric' ? 11.2 : 25) // 25 mph = 11.2 m/s
  };
}

// Get Google OAuth access token
async function getAccessToken() {
  return new Promise((resolve) => {
    chrome.identity.getAuthToken({ interactive: false }, (token) => {
      if (chrome.runtime.lastError) {
        console.error('Auth error:', chrome.runtime.lastError);
        resolve(null);
      } else {
        resolve(token);
      }
    });
  });
}

// Get or create calendar
async function getOrCreateCalendar(token) {
  try {
    // List calendars
    const response = await fetch('https://www.googleapis.com/calendar/v3/users/me/calendarList', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    if (!response.ok) throw new Error('Failed to list calendars');
    
    const data = await response.json();
    const existing = data.items?.find(cal => cal.summary === CALENDAR_NAME);
    
    if (existing) {
      return existing.id;
    }
    
    // Create new calendar
    const createResponse = await fetch('https://www.googleapis.com/calendar/v3/calendars', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        summary: CALENDAR_NAME,
        description: 'Automatically generated weather alerts and suggestions',
        timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
      })
    });
    
    if (!createResponse.ok) throw new Error('Failed to create calendar');
    
    const calendar = await createResponse.json();
    return calendar.id;
    
  } catch (error) {
    console.error('Error getting/creating calendar:', error);
    return null;
  }
}

// Normalize location format (convert province codes to country codes)
function normalizeLocation(location) {
  if (!location) return location;
  
  // Mapping of common province/state codes to country codes
  const PROVINCE_TO_COUNTRY = {
    // Canadian provinces
    'ON': 'CA', 'QC': 'CA', 'BC': 'CA', 'AB': 'CA', 'MB': 'CA',
    'SK': 'CA', 'NS': 'CA', 'NB': 'CA', 'NL': 'CA', 'PE': 'CA',
    'NT': 'CA', 'YT': 'CA', 'NU': 'CA',
    // US states (common ones)
    'NY': 'US', 'CA': 'US', 'TX': 'US', 'FL': 'US', 'IL': 'US',
    'PA': 'US', 'OH': 'US', 'GA': 'US', 'NC': 'US', 'MI': 'US',
  };
  
  // Check if location has a comma (city,code format)
  if (location.includes(',')) {
    const parts = location.split(',');
    if (parts.length === 2) {
      const city = parts[0].trim();
      const code = parts[1].trim().toUpperCase();
      
      // If it's a province code, convert to country code
      if (PROVINCE_TO_COUNTRY[code]) {
        const countryCode = PROVINCE_TO_COUNTRY[code];
        return `${city},${countryCode}`;
      }
    }
  }
  
  return location;
}

// Get weather forecast from OpenWeatherMap
async function getWeatherForecast(location, units, apiKey) {
  try {
    // Normalize location first
    const normalizedLocation = normalizeLocation(location);
    const url = `https://api.openweathermap.org/data/2.5/forecast?q=${encodeURIComponent(normalizedLocation)}&appid=${apiKey}&units=${units}&cnt=40`;
    const response = await fetch(url);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Weather API error:', response.status, errorText);
      throw new Error(`Weather API error: ${response.status}. Location "${location}" not found. Try "City,CountryCode" format (e.g., "Toronto,CA" or "New York,US")`);
    }
    
    const data = await response.json();
    
    // Group forecasts by day
    const dailyForecasts = {};
    data.list.forEach(item => {
      const date = new Date(item.dt * 1000);
      const dateKey = date.toISOString().split('T')[0];
      
      if (!dailyForecasts[dateKey]) {
        dailyForecasts[dateKey] = [];
      }
      
      dailyForecasts[dateKey].push({
        datetime: date,
        temp: item.main.temp,
        feels_like: item.main.feels_like,
        temp_min: item.main.temp_min,
        temp_max: item.main.temp_max,
        humidity: item.main.humidity,
        weather: item.weather[0],
        wind_speed: item.wind?.speed || 0,
        wind_gust: item.wind?.gust || 0,
        rain: item.rain?.['3h'] || 0,
        snow: item.snow?.['3h'] || 0,
        clouds: item.clouds?.all || 0
      });
    });
    
    return dailyForecasts;
  } catch (error) {
    console.error('Error fetching weather:', error);
    return null;
  }
}

// Generate weather events from forecast
function generateWeatherEvents(forecasts, settings) {
  const events = [];
  const tempUnit = settings.units === 'imperial' ? '°F' : '°C';
  const windUnit = settings.units === 'imperial' ? 'mph' : 'm/s';
  
  // Convert temperature thresholds if needed
  let minTemp = settings.minTemperature;
  let maxTemp = settings.maxTemperature;
  if (settings.units === 'metric') {
    // Config defaults are in Fahrenheit, convert if metric
    minTemp = (minTemp - 32) * 5 / 9;
    maxTemp = (maxTemp - 32) * 5 / 9;
  }
  
  // Convert wind threshold
  let windThreshold = settings.windThreshold;
  if (settings.units === 'metric') {
    windThreshold = windThreshold * 0.447; // mph to m/s
  }
  
  Object.keys(forecasts).forEach(dateKey => {
    const dayForecasts = forecasts[dateKey];
    if (!dayForecasts || dayForecasts.length === 0) return;
    
    // Calculate daily aggregates
    const temps = dayForecasts.map(f => f.temp);
    const rainTotal = dayForecasts.reduce((sum, f) => sum + f.rain, 0);
    const snowTotal = dayForecasts.reduce((sum, f) => sum + f.snow, 0);
    const windSpeeds = dayForecasts.map(f => f.wind_speed);
    const windGusts = dayForecasts.map(f => f.wind_gust).filter(g => g > 0);
    
    const tempMin = Math.min(...temps);
    const tempMax = Math.max(...temps);
    const windMax = Math.max(...windSpeeds);
    const windGustMax = windGusts.length > 0 ? Math.max(...windGusts) : 0;
    const conditions = dayForecasts[0].weather.main;
    
    const baseDate = new Date(dateKey + 'T00:00:00');
    
    // Helper function to create date with hours
    const createDate = (hours) => {
      const d = new Date(baseDate);
      d.setHours(hours, 0, 0, 0);
      return d;
    };
    
    // Cold alert
    if (tempMin < minTemp) {
      events.push({
        type: 'cold_alert',
        title: `❄️ Cold Weather Alert - ${Math.round(tempMin)}${tempUnit}`,
        description: `Very cold temperatures expected. Low: ${Math.round(tempMin)}${tempUnit}, High: ${Math.round(tempMax)}${tempUnit}. Dress warmly!`,
        start: createDate(7),
        end: createDate(9)
      });
    }
    
    // Heat alert
    if (tempMax > maxTemp) {
      events.push({
        type: 'heat_alert',
        title: `🔥 Heat Alert - ${Math.round(tempMax)}${tempUnit}`,
        description: `Hot temperatures expected. High: ${Math.round(tempMax)}${tempUnit}, Low: ${Math.round(tempMin)}${tempUnit}. Stay hydrated!`,
        start: createDate(10),
        end: createDate(18)
      });
    }
    
    // Rain alert
    if (rainTotal >= settings.rainThreshold) {
      events.push({
        type: 'rain_alert',
        title: `🌧️ Rain Expected - ${rainTotal.toFixed(1)}mm`,
        description: `Significant rainfall expected (${rainTotal.toFixed(1)}mm). Remember to bring an umbrella!`,
        start: createDate(6),
        end: createDate(22)
      });
    }
    
    // Snow alert
    if (snowTotal >= settings.snowThreshold) {
      events.push({
        type: 'snow_alert',
        title: `❄️ Snow Expected - ${snowTotal.toFixed(1)}mm`,
        description: `Snowfall expected (${snowTotal.toFixed(1)}mm). Allow extra travel time!`,
        start: createDate(6),
        end: createDate(22)
      });
    }
    
    // Wind alert
    if (windMax >= windThreshold) {
      events.push({
        type: 'wind_alert',
        title: `💨 High Winds - ${Math.round(windMax)} ${windUnit}`,
        description: `Strong winds expected (up to ${Math.round(windMax)} ${windUnit}, gusts up to ${Math.round(windGustMax)} ${windUnit}).`,
        start: createDate(8),
        end: createDate(20)
      });
    }
    
    // UV alert (simplified)
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    if (conditions === 'Clear' && baseDate >= today) {
      events.push({
        type: 'uv_alert',
        title: `☀️ High UV Expected`,
        description: `Clear/sunny conditions expected. Remember sunscreen and UV protection!`,
        start: createDate(10),
        end: createDate(16)
      });
    }
    
    // Nice weather
    const niceTempMin = settings.units === 'imperial' ? 60 : 15.5;
    const niceTempMax = settings.units === 'imperial' ? 80 : 26.7;
    const niceWindMax = settings.units === 'imperial' ? 15 : 6.7;
    
    if (tempMin >= niceTempMin && tempMax <= niceTempMax && 
        rainTotal < 1 && windMax < niceWindMax &&
        ['Clear', 'Sunny'].includes(conditions)) {
      events.push({
        type: 'nice_weather',
        title: `☀️ Perfect Weather Day!`,
        description: `Great weather expected! Temp: ${Math.round(tempMin)}${tempUnit} - ${Math.round(tempMax)}${tempUnit}. Perfect for outdoor activities!`,
        start: createDate(9),
        end: createDate(17)
      });
    }
  });
  
  return events;
}

// Sync events to Google Calendar
async function syncEventsToCalendar(token, calendarId, events) {
  try {
    // Get existing events
    const now = new Date();
    const future = new Date();
    future.setDate(future.getDate() + 5);
    
    const listResponse = await fetch(
      `https://www.googleapis.com/calendar/v3/calendars/${calendarId}/events?` +
      `timeMin=${now.toISOString()}&timeMax=${future.toISOString()}&singleEvents=true`,
      {
        headers: { 'Authorization': `Bearer ${token}` }
      }
    );
    
    if (!listResponse.ok) throw new Error('Failed to list events');
    
    const existingEvents = await listResponse.json();
    const existingByKey = {};
    
    existingEvents.items?.forEach(event => {
      const key = extractEventKey(event.summary, event.start?.dateTime);
      if (key) existingByKey[key] = event;
    });
    
    const currentKeys = new Set();
    
    // Create or update events
    for (const event of events) {
      const key = `${event.type}_${event.start.toISOString().split('T')[0]}`;
      currentKeys.add(key);
      
      if (existingByKey[key]) {
        // Update existing event
        await fetch(
          `https://www.googleapis.com/calendar/v3/calendars/${calendarId}/events/${existingByKey[key].id}`,
          {
            method: 'PUT',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              summary: event.title,
              description: event.description,
              start: { 
                dateTime: event.start.toISOString(),
                timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
              },
              end: { 
                dateTime: event.end.toISOString(),
                timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
              }
            })
          }
        );
      } else {
        // Create new event
        await fetch(
          `https://www.googleapis.com/calendar/v3/calendars/${calendarId}/events`,
          {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              summary: event.title,
              description: event.description,
              start: { 
                dateTime: event.start.toISOString(),
                timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
              },
              end: { 
                dateTime: event.end.toISOString(),
                timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone
              }
            })
          }
        );
      }
    }
    
    // Delete outdated events
    for (const [key, event] of Object.entries(existingByKey)) {
      if (!currentKeys.has(key)) {
        const eventDate = new Date(event.start?.dateTime);
        if (eventDate > now) {
          await fetch(
            `https://www.googleapis.com/calendar/v3/calendars/${calendarId}/events/${event.id}`,
            {
              method: 'DELETE',
              headers: { 'Authorization': `Bearer ${token}` }
            }
          );
        }
      }
    }
    
  } catch (error) {
    console.error('Error syncing events:', error);
  }
}

// Extract event key from title
function extractEventKey(title, startTime) {
  if (!title || !startTime) return null;
  const date = new Date(startTime).toISOString().split('T')[0];
  
  if (title.includes('Cold Weather') || title.includes('❄️ Cold')) return `cold_alert_${date}`;
  if (title.includes('Heat Alert') || title.includes('🔥 Heat')) return `heat_alert_${date}`;
  if (title.includes('Rain Expected') || title.includes('🌧️ Rain')) return `rain_alert_${date}`;
  if (title.includes('Snow Expected') || title.includes('❄️ Snow')) return `snow_alert_${date}`;
  if (title.includes('High Winds') || title.includes('💨 High')) return `wind_alert_${date}`;
  if (title.includes('High UV') || title.includes('☀️ High UV')) return `uv_alert_${date}`;
  if (title.includes('Perfect Weather') || title.includes('☀️ Perfect')) return `nice_weather_${date}`;
  
  return null;
}

// Manual sync trigger (for popup)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'sync') {
    syncWeatherEvents().then(() => {
      sendResponse({ success: true });
    }).catch((error) => {
      sendResponse({ success: false, error: error.message });
    });
    return true; // Will respond asynchronously
  }
});

