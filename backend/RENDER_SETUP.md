# Deploy Backend to Render - Simple Guide

## Why Render?
- ✅ Automatic deployments
- ✅ Free tier available
- ✅ No SSH needed
- ✅ Automatic HTTPS
- ✅ Easy to set up

## Step 1: Create Render Account
1. Go to https://render.com
2. Sign up (free account works)

## Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository (or use manual deploy)
3. Or upload files directly

## Step 3: Configure Service
- **Name**: `chickenbites-api`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python start.py`
- **Port**: `8000` (or leave default)

## Step 4: Set Environment Variables
In Render dashboard, add these:
- `PORT` = `8000`
- `DB_HOST` = `srv2049.hstgr.io`
- `DB_NAME` = `u761984878_csc4`
- `DB_USER` = `u761984878_csc4`
- `DB_PASSWORD` = `Azraelcisco123!`

## Step 5: Deploy
1. Render will automatically build and deploy
2. You'll get a URL like: `https://chickenbites-api.onrender.com`
3. Update your frontend `api_client.py` with this URL

## Step 6: Update Frontend
In `frontend/api_client.py`:
```python
API_BASE_URL = 'https://chickenbites-api.onrender.com'
```

## That's It!
- Backend runs automatically on Render
- No SSH, no manual commands
- Free tier available
- Auto-deploys on code changes

