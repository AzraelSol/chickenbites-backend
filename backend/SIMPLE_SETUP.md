# Simple Setup - Backend on Hostinger, Frontend Here

## Backend on Hostinger (One-Time Setup)

### Step 1: Upload Backend Files
Upload all files from the `backend/` folder to your Hostinger:
- Upload to: `public_html/csc4/` (or your subdomain folder)

### Step 2: Use Hostinger Python App (Easiest - Keeps Running Automatically)

1. **Login to Hostinger hPanel**
2. **Go to "Python App" or "Applications"**
3. **Create New Python App:**
   - App name: `chickenbites-api`
   - Python version: `3.x`
   - **Startup file:** `start.py` (or `index.py`)
   - **App directory:** `/public_html/csc4` (where you uploaded backend)
4. **Install dependencies:**
   - In Python App settings, add: `mysql-connector-python`
5. **Start the app** - It will run automatically and stay running!

### Step 3: Update Frontend API URL

In `frontend/api_client.py`, set:
```python
API_BASE_URL = 'http://csc4.gisrabies.com'
# or if using subdirectory:
API_BASE_URL = 'http://csc4.gisrabies.com/api'
```

### Step 4: Update Backend config.py on Hostinger

Edit `config.py` on Hostinger:
- Set `DB_HOST` to `localhost`
- Update database credentials

## That's It!

- **Backend**: Runs automatically on Hostinger (via Python App)
- **Frontend**: Run `python main.py` on your computer
- **No SSH needed**: Everything through hPanel
- **Stays running**: Python App keeps it running automatically

## Test It

Visit in browser:
```
http://csc4.gisrabies.com/api/health
```

If you see JSON response, it's working!

