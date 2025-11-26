# How to Host Your Privacy Policy

The Chrome Web Store requires a publicly accessible URL for your privacy policy. Here are several easy options:

## Option 1: GitHub Pages (Recommended - Free)

1. **Create a GitHub repository** (if you don't have one)
   - Go to github.com and create a new repository
   - Name it something like "weather-calendar-agent" or "privacy-policy"

2. **Upload the privacy policy**
   - Create a file named `privacy-policy.html` or `privacy.html`
   - Copy the content from `PRIVACY_POLICY.html` in this folder
   - Upload it to your repository

3. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Select the branch (usually `main` or `master`)
   - Save

4. **Get your URL**
   - Your privacy policy will be available at:
   - `https://yourusername.github.io/repository-name/privacy-policy.html`
   - Or if you name it `privacy.html`:
   - `https://yourusername.github.io/repository-name/privacy.html`

## Option 2: GitHub Gist (Free & Quick)

1. Go to gist.github.com
2. Create a new gist
3. Name the file `privacy-policy.html`
4. Paste the content from `PRIVACY_POLICY.html`
5. Click "Create public gist"
6. Use the "Raw" URL as your privacy policy URL
   - Click "Raw" button on the gist page
   - Copy that URL

## Option 3: Your Own Website

If you have a website:
1. Upload `PRIVACY_POLICY.html` to your web server
2. Access it via: `https://yourdomain.com/privacy-policy.html`

## Option 4: Netlify Drop (Free)

1. Go to app.netlify.com/drop
2. Drag and drop the `PRIVACY_POLICY.html` file
3. Get your URL: `https://random-name-123.netlify.app/privacy-policy.html`
4. Rename the file to `index.html` for a cleaner URL

## Option 5: Google Sites (Free)

1. Go to sites.google.com
2. Create a new site
3. Copy and paste the privacy policy content
4. Publish the site
5. Use the published URL

## Quick Setup with GitHub Pages (Step-by-Step)

1. **Create repository:**
   ```
   - Go to github.com/new
   - Repository name: privacy-policy (or any name)
   - Make it public
   - Create repository
   ```

2. **Upload file:**
   ```
   - Click "Add file" → "Upload files"
   - Upload PRIVACY_POLICY.html
   - Rename it to index.html (for cleaner URL)
   - Commit changes
   ```

3. **Enable Pages:**
   ```
   - Settings → Pages
   - Source: Deploy from a branch
   - Branch: main, folder: / (root)
   - Save
   ```

4. **Get URL:**
   ```
   Your URL will be:
   https://yourusername.github.io/privacy-policy/
   ```

## What to Enter in Chrome Web Store

Once you have your privacy policy URL, enter it in the "Privacy policy URL*" field.

**Example URLs:**
- `https://yourusername.github.io/weather-calendar-agent/privacy-policy.html`
- `https://gist.githubusercontent.com/username/gist-id/raw/privacy-policy.html`
- `https://yourdomain.com/privacy-policy.html`

## Important Notes

- ✅ The URL must be publicly accessible (no login required)
- ✅ The URL must use HTTPS (secure connection)
- ✅ The page must be accessible from any browser
- ✅ The content should match what you described in the data usage form

## Testing Your Privacy Policy URL

Before submitting:
1. Open the URL in an incognito/private browser window
2. Verify it loads correctly
3. Make sure it's accessible without login
4. Check that it uses HTTPS

