# Chrome Web Store Submission Checklist

## Pre-Submission Requirements

### ✅ Code & Files
- [x] All code files present and working
- [x] manifest.json properly configured
- [x] Icons created (icon.png - 128x128px)
- [x] No console errors
- [x] Extension tested and working

### 📝 Store Listing Information

#### Required Information
- [ ] **Name:** Weather Calendar Agent
- [ ] **Short Description:** (132 chars max) - See STORE_LISTING.md
- [ ] **Detailed Description:** - See STORE_LISTING.md
- [ ] **Category:** Productivity
- [ ] **Language:** English (United States)

#### Images Required
- [ ] **Icon:** 128x128px PNG (icon.png)
- [ ] **Screenshots:** At least 1, up to 5 (1280x800px or 640x400px)
  - [ ] Screenshot 1: Main popup interface
  - [ ] Screenshot 2: Location autocomplete
  - [ ] Screenshot 3: Calendar integration
  - [ ] Screenshot 4: Settings
  - [ ] Screenshot 5: Event details
- [ ] **Small Promotional Tile:** 440x280px (optional but recommended)
- [ ] **Large Promotional Tile:** 920x680px (optional but recommended)

#### Privacy & Legal
- [ ] **Privacy Policy:** Required (see PRIVACY_POLICY.md)
  - Host on a publicly accessible URL
  - Add privacy policy URL to store listing
- [ ] **Single Purpose:** Extension has a single, clear purpose ✓
- [ ] **User Data:** Declare what data is collected (see PRIVACY_POLICY.md)

#### Permissions Justification
- [ ] **Identity:** "Required to authenticate with Google Calendar API to create weather events"
- [ ] **Storage:** "Stores user preferences (location, units, API key) locally"
- [ ] **Alarms:** "Schedules automatic weather updates every 15 minutes"
- [ ] **Host Permissions:** 
  - "https://www.googleapis.com/* - Google Calendar API access"
  - "https://api.openweathermap.org/* - Weather data API access"

### 🔍 Testing Checklist
- [ ] Extension loads without errors
- [ ] OAuth authentication works
- [ ] Location autocomplete functions
- [ ] Weather API calls succeed
- [ ] Calendar events are created correctly
- [ ] Automatic sync works (15-minute intervals)
- [ ] Manual sync button works
- [ ] Settings are saved and loaded
- [ ] Error handling works properly
- [ ] Works on different Chrome versions

### 📋 Store Listing Details

#### Category & Classification
- **Category:** Productivity
- **Content Rating:** Everyone
- **Mature Content:** No

#### Distribution
- **Visibility:** Public (or Unlisted for testing)
- **Regions:** All regions (or specific if needed)
- **Pricing:** Free

#### Additional Information
- **Support URL:** (GitHub repository or support page)
- **Homepage URL:** (GitHub repository)
- **Privacy Policy URL:** (Required - must be publicly accessible)

### 🚀 Submission Steps

1. **Prepare Assets**
   - Create all required images
   - Write privacy policy and host it
   - Prepare store listing text

2. **Developer Dashboard**
   - Go to Chrome Web Store Developer Dashboard
   - Click "Add new item"
   - Upload extension ZIP file

3. **Fill Store Listing**
   - Upload icon
   - Upload screenshots
   - Fill in description
   - Add privacy policy URL
   - Set category and pricing

4. **Submit for Review**
   - Review all information
   - Submit for review
   - Wait for approval (typically 1-3 business days)

### 📝 Notes for Reviewers

**What the extension does:**
- Automatically syncs weather forecasts to Google Calendar
- Creates weather alert events based on forecast data
- Updates events every 15 minutes

**Why permissions are needed:**
- Identity: Google Calendar OAuth authentication
- Storage: Local preference storage
- Alarms: Scheduled background updates
- Host permissions: API access for Google Calendar and OpenWeatherMap

**User data handling:**
- All data stored locally
- No data collection
- No external servers
- Privacy policy provided

### ⚠️ Common Rejection Reasons to Avoid

1. **Missing Privacy Policy** - Must be publicly accessible
2. **Unclear Permissions** - Justify all permissions clearly
3. **Poor Description** - Be clear about what the extension does
4. **Missing Screenshots** - Include at least 1 screenshot
5. **Broken Functionality** - Test thoroughly before submission
6. **Misleading Claims** - Be honest about features

### 📞 Support Information

**For Users:**
- Include support URL in store listing
- GitHub issues for bug reports
- Clear documentation in README

**For Reviewers:**
- Code is open source and reviewable
- All permissions are necessary and justified
- Privacy policy clearly states no data collection

