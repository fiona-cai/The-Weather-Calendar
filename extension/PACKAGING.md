# Packaging Extension for Chrome Web Store

## Steps to Create Extension Package

### 1. Prepare Files

Ensure all files are in the `extension` folder:
- manifest.json
- background.js
- popup.html
- popup.js
- icons/icon.png (128x128px)

### 2. Remove Unnecessary Files

Before packaging, remove:
- README files (optional - can keep)
- .git files
- Development files
- Test files

### 3. Create ZIP File

**On Mac/Linux:**
```bash
cd extension
zip -r ../weather-calendar-agent.zip . -x "*.git*" "*.md" "*.DS_Store"
```

**On Windows:**
1. Select all files in the extension folder
2. Right-click → Send to → Compressed (zipped) folder
3. Rename to `weather-calendar-agent.zip`

### 4. Verify ZIP Contents

The ZIP should contain:
```
weather-calendar-agent.zip
├── manifest.json
├── background.js
├── popup.html
├── popup.js
└── icons/
    └── icon.png
```

### 5. Test the ZIP

1. Extract the ZIP to a temporary folder
2. Load it in Chrome as an unpacked extension
3. Verify everything works
4. Delete the temporary folder

### 6. Upload to Chrome Web Store

1. Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
2. Click "New Item"
3. Upload the ZIP file
4. Fill in store listing information
5. Submit for review

## File Size Considerations

- Keep ZIP under 10MB (should be much smaller)
- Optimize images if needed
- Remove any unnecessary files

## Version Numbering

Update version in manifest.json:
- Format: "major.minor.patch" (e.g., "1.0.0")
- Increment for updates:
  - Patch (1.0.1): Bug fixes
  - Minor (1.1.0): New features
  - Major (2.0.0): Breaking changes

## Checklist Before Submission

- [ ] All files present
- [ ] manifest.json version updated
- [ ] Icon file included (icon.png)
- [ ] ZIP file created and tested
- [ ] No console errors
- [ ] Extension works when loaded from ZIP
- [ ] Privacy policy hosted and accessible
- [ ] Store listing information prepared

