# Chrome Web Store Submission Guide

## Quick Start

This guide contains everything you need to submit Weather Calendar Agent to the Chrome Web Store.

## 📋 Required Documents

1. **STORE_DESCRIPTION.txt** - Copy-paste ready store listing text
2. **PRIVACY_POLICY.md** - Privacy policy (must be hosted online)
3. **STORE_LISTING.md** - Detailed store listing information
4. **STORE_ASSETS.md** - Image requirements and specifications
5. **SUBMISSION_CHECKLIST.md** - Complete checklist for submission
6. **PACKAGING.md** - Instructions for creating the ZIP file

## 🚀 Submission Steps

### Step 1: Host Privacy Policy
1. Copy content from `PRIVACY_POLICY.md`
2. Host it on a publicly accessible URL (GitHub Pages, your website, etc.)
3. Note the URL - you'll need it for the store listing

### Step 2: Create Images
Refer to `STORE_ASSETS.md` for specifications:
- Icon: 128x128px (already have icon.png)
- Screenshots: At least 1, up to 5 (1280x800px or 640x400px)
- Promotional tiles: Optional but recommended

### Step 3: Package Extension
Follow instructions in `PACKAGING.md`:
1. Create ZIP file of extension folder
2. Test the ZIP by loading it as unpacked extension
3. Verify everything works

### Step 4: Prepare Store Listing
1. Open `STORE_DESCRIPTION.txt`
2. Copy the short description (132 chars)
3. Copy the detailed description
4. Prepare screenshots

### Step 5: Submit to Chrome Web Store
1. Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
2. Click "New Item"
3. Upload your ZIP file
4. Fill in all required fields:
   - Name: Weather Calendar Agent
   - Short description: (from STORE_DESCRIPTION.txt)
   - Detailed description: (from STORE_DESCRIPTION.txt)
   - Category: Productivity
   - Language: English (United States)
   - Privacy Policy URL: (your hosted privacy policy)
   - Support URL: (optional - GitHub repo)
   - Homepage URL: (optional - GitHub repo)
5. Upload icon and screenshots
6. Review all information
7. Submit for review

## 📝 Key Information Summary

**Extension Name:** Weather Calendar Agent

**Category:** Productivity

**Short Description (132 chars):**
```
Automatically syncs weather alerts and suggestions to your Google Calendar. Get notified about rain, snow, extreme temperatures, and perfect weather days!
```

**Permissions Justification:**
- **Identity:** Required for Google Calendar OAuth authentication
- **Storage:** Stores user preferences locally (location, units, API key)
- **Alarms:** Schedules automatic weather updates every 15 minutes
- **Host Permissions:** 
  - `https://www.googleapis.com/*` - Google Calendar API
  - `https://api.openweathermap.org/*` - Weather data API

**Privacy:**
- All data stored locally
- No data collection
- No external servers
- Privacy policy required

## ✅ Pre-Submission Checklist

- [ ] Privacy policy hosted and accessible
- [ ] Extension ZIP file created and tested
- [ ] Icon file ready (128x128px)
- [ ] At least 1 screenshot prepared
- [ ] Store listing text prepared
- [ ] All permissions justified
- [ ] Extension tested thoroughly
- [ ] No console errors
- [ ] manifest.json version is correct (1.0.0)

## 📞 Support Information

**For Store Listing:**
- Support URL: (Add your GitHub repo or support page)
- Homepage URL: (Add your GitHub repo)

**For Users:**
- Clear instructions in README
- Support through GitHub issues
- Privacy policy clearly states data handling

## ⚠️ Important Notes

1. **Privacy Policy is REQUIRED** - Must be publicly accessible
2. **Justify All Permissions** - Explain why each permission is needed
3. **Test Thoroughly** - Extension must work without errors
4. **Clear Description** - Be specific about what the extension does
5. **Screenshots Help** - Include at least 1 screenshot showing the extension in action

## 🎯 Review Timeline

- Initial review: 1-3 business days
- Updates: Usually faster (1-2 days)
- Rejections: Fix issues and resubmit

## 📚 Additional Resources

- [Chrome Web Store Developer Documentation](https://developer.chrome.com/docs/webstore/)
- [Chrome Web Store Policies](https://developer.chrome.com/docs/webstore/program-policies/)
- [Extension Quality Guidelines](https://developer.chrome.com/docs/webstore/user-data/)

## 🎉 After Approval

Once approved:
1. Extension will be live on Chrome Web Store
2. Users can install and rate
3. Monitor reviews and feedback
4. Plan updates based on user feedback

Good luck with your submission! 🚀

