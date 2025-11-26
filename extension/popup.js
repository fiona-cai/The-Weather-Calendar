// Popup script for Weather Calendar Agent

let suggestionTimeout = null;
let currentSuggestions = [];
let selectedIndex = -1;

document.addEventListener('DOMContentLoaded', async () => {
  // Load saved settings
  await loadSettings();
  
  // Check auth status
  checkAuthStatus();
  
  // Setup event listeners
  document.getElementById('authBtn').addEventListener('click', authorize);
  document.getElementById('saveBtn').addEventListener('click', saveSettings);
  document.getElementById('syncBtn').addEventListener('click', syncNow);
  document.getElementById('togglePassword').addEventListener('click', togglePasswordVisibility);
  
  // Setup location autocomplete
  setupLocationAutocomplete();
  
  // Update last sync time
  updateLastSync();
  
  // Auto-update last sync every minute
  setInterval(updateLastSync, 60000);
  
  // Close suggestions when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.autocomplete-wrapper')) {
      hideSuggestions();
    }
  });
});

// Toggle password visibility
function togglePasswordVisibility() {
  const input = document.getElementById('weatherApiKey');
  const toggle = document.getElementById('togglePassword');
  
  if (input.type === 'password') {
    input.type = 'text';
    toggle.textContent = '🙈';
  } else {
    input.type = 'password';
    toggle.textContent = '👁️';
  }
}

// Setup location autocomplete
function setupLocationAutocomplete() {
  const locationInput = document.getElementById('location');
  
  locationInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();
    
    // Clear previous timeout
    if (suggestionTimeout) {
      clearTimeout(suggestionTimeout);
    }
    
    // Hide suggestions if input is empty
    if (query.length < 2) {
      hideSuggestions();
      return;
    }
    
    // Debounce API calls
    suggestionTimeout = setTimeout(() => {
      searchLocations(query);
    }, 300);
  });
  
  locationInput.addEventListener('keydown', (e) => {
    const suggestions = document.getElementById('suggestions');
    
    if (!suggestions.classList.contains('show') || currentSuggestions.length === 0) {
      return;
    }
    
    switch(e.key) {
      case 'ArrowDown':
        e.preventDefault();
        selectedIndex = Math.min(selectedIndex + 1, currentSuggestions.length - 1);
        updateHighlight();
        break;
      case 'ArrowUp':
        e.preventDefault();
        selectedIndex = Math.max(selectedIndex - 1, -1);
        updateHighlight();
        break;
      case 'Enter':
        e.preventDefault();
        if (selectedIndex >= 0 && currentSuggestions[selectedIndex]) {
          selectSuggestion(currentSuggestions[selectedIndex]);
        }
        break;
      case 'Escape':
        e.preventDefault();
        hideSuggestions();
        break;
    }
  });
}

// Search for locations using OpenWeatherMap Geocoding API
async function searchLocations(query) {
  const suggestionsEl = document.getElementById('suggestions');
  suggestionsEl.innerHTML = '<div class="loading-suggestions">🔍 Searching...</div>';
  suggestionsEl.classList.add('show');
  
  const result = await chrome.storage.local.get('weatherApiKey');
  const apiKey = result.weatherApiKey;
  
  if (!apiKey) {
    // Show common cities if no API key
    showCommonCities(query);
    return;
  }
  
  try {
    const url = `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(query)}&limit=5&appid=${apiKey}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error('API request failed');
    }
    
    const locations = await response.json();
    displaySuggestions(locations);
  } catch (error) {
    console.error('Error fetching locations:', error);
    // Fallback to common cities
    showCommonCities(query);
  }
}

// Show common cities as fallback
function showCommonCities(query) {
  const commonCities = [
    { name: 'New York', state: 'NY', country: 'US' },
    { name: 'Los Angeles', state: 'CA', country: 'US' },
    { name: 'Chicago', state: 'IL', country: 'US' },
    { name: 'Houston', state: 'TX', country: 'US' },
    { name: 'Toronto', state: 'ON', country: 'CA' },
    { name: 'Vancouver', state: 'BC', country: 'CA' },
    { name: 'London', country: 'GB' },
    { name: 'Paris', country: 'FR' },
    { name: 'Tokyo', country: 'JP' },
    { name: 'Sydney', country: 'AU' },
  ];
  
  const filtered = commonCities.filter(city => 
    city.name.toLowerCase().includes(query.toLowerCase())
  ).slice(0, 5);
  
  const formatted = filtered.map(city => ({
    name: city.name,
    country: city.country,
    state: city.state,
    formatted: city.state ? `${city.name},${city.state},${city.country}` : `${city.name},${city.country}`
  }));
  
  displaySuggestions(formatted);
}

// Display suggestions
function displaySuggestions(locations) {
  const suggestionsEl = document.getElementById('suggestions');
  currentSuggestions = locations;
  selectedIndex = -1;
  
  if (locations.length === 0) {
    suggestionsEl.innerHTML = '<div class="no-suggestions">No locations found</div>';
    suggestionsEl.classList.add('show');
    return;
  }
  
  suggestionsEl.innerHTML = locations.map((loc, index) => {
    let displayName, country, state, countryName, details, formatted;
    
    if (loc.formatted) {
      // Fallback format
      const parts = loc.formatted.split(',');
      displayName = parts[0];
      state = parts[1] || '';
      country = parts[2] || parts[1] || '';
      formatted = loc.formatted;
    } else {
      // API format
      displayName = loc.name || 'Unknown';
      country = loc.country || '';
      state = loc.state || '';
      formatted = state ? `${displayName},${state},${country}` : `${displayName},${country}`;
    }
    
    countryName = getCountryName(country);
    details = state ? `${state}, ${countryName}` : countryName;
    
    return `
      <div class="suggestion-item" data-index="${index}" data-value="${formatted}">
        <span class="suggestion-icon">📍</span>
        <div class="suggestion-text">
          <div class="suggestion-name">${displayName}</div>
          <div class="suggestion-details">${details}</div>
        </div>
      </div>
    `;
  }).join('');
  
  // Add click handlers
  suggestionsEl.querySelectorAll('.suggestion-item').forEach((item, index) => {
    item.addEventListener('click', () => {
      selectSuggestion(locations[index]);
    });
  });
  
  suggestionsEl.classList.add('show');
}

// Update highlight for keyboard navigation
function updateHighlight() {
  const items = document.querySelectorAll('.suggestion-item');
  items.forEach((item, index) => {
    if (index === selectedIndex) {
      item.classList.add('highlighted');
      item.scrollIntoView({ block: 'nearest' });
    } else {
      item.classList.remove('highlighted');
    }
  });
}

// Select a suggestion
function selectSuggestion(location) {
  let formatted;
  
  if (location.formatted) {
    formatted = location.formatted;
  } else if (location.name && location.country) {
    // Format from API response
    if (location.state) {
      formatted = `${location.name},${location.state},${location.country}`;
    } else {
      formatted = `${location.name},${location.country}`;
    }
  } else {
    formatted = location;
  }
  
  document.getElementById('location').value = formatted;
  hideSuggestions();
}

// Hide suggestions
function hideSuggestions() {
  const suggestionsEl = document.getElementById('suggestions');
  suggestionsEl.classList.remove('show');
  selectedIndex = -1;
  currentSuggestions = [];
}

// Get country name from code
function getCountryName(code) {
  const countries = {
    'US': 'United States',
    'CA': 'Canada',
    'GB': 'United Kingdom',
    'FR': 'France',
    'DE': 'Germany',
    'IT': 'Italy',
    'ES': 'Spain',
    'JP': 'Japan',
    'CN': 'China',
    'AU': 'Australia',
    'BR': 'Brazil',
    'IN': 'India',
    'MX': 'Mexico',
  };
  return countries[code] || code;
}

// Load settings from storage
async function loadSettings() {
  const result = await chrome.storage.local.get([
    'location',
    'weatherApiKey',
    'units'
  ]);
  
  if (result.location) {
    document.getElementById('location').value = result.location;
  }
  if (result.weatherApiKey) {
    document.getElementById('weatherApiKey').value = result.weatherApiKey;
  }
  if (result.units) {
    document.getElementById('units').value = result.units;
  }
}

// Check Google Calendar auth status
async function checkAuthStatus() {
  chrome.identity.getAuthToken({ interactive: false }, (token) => {
    const authStatus = document.getElementById('authStatus');
    const authBtn = document.getElementById('authBtn');
    
    if (chrome.runtime.lastError || !token) {
      authStatus.innerHTML = '<span class="auth-status-icon">⚠️</span><span>Not authorized. Click to authorize.</span>';
      authStatus.className = 'auth-status error';
      authStatus.style.display = 'flex';
      authBtn.innerHTML = '<span>🔐</span><span>Authorize Google Calendar</span>';
    } else {
      authStatus.innerHTML = '<span class="auth-status-icon">✓</span><span>Successfully authorized</span>';
      authStatus.className = 'auth-status success';
      authStatus.style.display = 'flex';
      authBtn.innerHTML = '<span>🔓</span><span>Re-authorize</span>';
      document.getElementById('syncBtn').disabled = false;
    }
  });
}

// Authorize with Google Calendar
function authorize() {
  const authBtn = document.getElementById('authBtn');
  const originalText = authBtn.innerHTML;
  
  authBtn.innerHTML = '<span class="loading"></span><span>Authorizing...</span>';
  authBtn.disabled = true;
  
  chrome.identity.getAuthToken({ interactive: true }, (token) => {
    authBtn.disabled = false;
    
    if (chrome.runtime.lastError) {
      showStatus('Authorization failed: ' + chrome.runtime.lastError.message, 'error');
      authBtn.innerHTML = originalText;
    } else {
      showStatus('✓ Successfully authorized!', 'success');
      checkAuthStatus();
    }
  });
}

// Save settings
async function saveSettings() {
  const location = document.getElementById('location').value.trim();
  const weatherApiKey = document.getElementById('weatherApiKey').value.trim();
  const units = document.getElementById('units').value;
  const saveBtn = document.getElementById('saveBtn');
  
  if (!location) {
    showStatus('⚠️ Please enter a location', 'error');
    document.getElementById('location').focus();
    return;
  }
  
  if (!weatherApiKey) {
    showStatus('⚠️ Please enter your OpenWeatherMap API key', 'error');
    document.getElementById('weatherApiKey').focus();
    return;
  }
  
  const originalText = saveBtn.innerHTML;
  saveBtn.innerHTML = '<span class="loading"></span><span>Saving...</span>';
  saveBtn.disabled = true;
  
  await chrome.storage.local.set({
    location,
    weatherApiKey,
    units
  });
  
  saveBtn.innerHTML = originalText;
  saveBtn.disabled = false;
  showStatus('✓ Settings saved successfully!', 'success');
  
  // Enable sync button if authorized
  chrome.identity.getAuthToken({ interactive: false }, (token) => {
    if (token) {
      document.getElementById('syncBtn').disabled = false;
    }
  });
}

// Sync now
async function syncNow() {
  const syncBtn = document.getElementById('syncBtn');
  syncBtn.disabled = true;
  syncBtn.innerHTML = '<span class="loading"></span><span>Syncing...</span>';
  
  showStatus('🔄 Syncing weather events to your calendar...', 'info');
  
  // Send message to background script
  chrome.runtime.sendMessage({ action: 'sync' }, (response) => {
    syncBtn.disabled = false;
    syncBtn.innerHTML = '<span>🔄</span><span>Sync Now</span>';
    
    if (chrome.runtime.lastError) {
      let errorMsg = chrome.runtime.lastError.message;
      if (errorMsg.includes('404') || errorMsg.includes('not found')) {
        errorMsg = 'Location not found. Use format "City,CountryCode" (e.g., "Toronto,CA" or "New York,US"). Province codes like "ON" are automatically converted.';
      }
      showStatus('❌ Sync failed: ' + errorMsg, 'error');
    } else if (response && !response.success) {
      showStatus('❌ Sync failed: ' + (response.error || 'Unknown error'), 'error');
    } else {
      showStatus('✓ Sync completed successfully!', 'success');
      updateLastSync();
    }
  });
}

// Show status message
function showStatus(message, type) {
  const status = document.getElementById('status');
  status.textContent = message;
  status.className = `status ${type}`;
  status.style.display = 'block';
  
  // Auto-hide success messages after 4 seconds
  if (type === 'success') {
    setTimeout(() => {
      status.style.display = 'none';
    }, 4000);
  }
  
  // Auto-hide info messages after 5 seconds
  if (type === 'info') {
    setTimeout(() => {
      if (status.textContent === message) {
        status.style.display = 'none';
      }
    }, 5000);
  }
}

// Update last sync display
async function updateLastSync() {
  const result = await chrome.storage.local.get('lastSync');
  const lastSyncEl = document.getElementById('lastSync');
  
  if (result.lastSync) {
    const date = new Date(result.lastSync);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    
    let timeStr;
    if (diffMins < 1) {
      timeStr = 'Just now';
    } else if (diffMins < 60) {
      timeStr = `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
    } else if (diffHours < 24) {
      timeStr = `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
    } else {
      timeStr = date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }
    
    lastSyncEl.textContent = timeStr;
  } else {
    lastSyncEl.textContent = 'No syncs yet';
  }
}
