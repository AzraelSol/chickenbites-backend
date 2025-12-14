# Complete Setup Guide: GitHub + Render

## Part 1: Create GitHub Repository

### Step 1: Create GitHub Account (if you don't have one)
1. Go to https://github.com
2. Sign up for a free account
3. Verify your email

### Step 2: Create New Repository
1. Click the **"+"** icon in top right → **"New repository"**
2. Repository name: `chickenbites-backend`
3. Description: `Chicken Bites API Backend`
4. Choose: **Private** (or Public, your choice)
5. **DO NOT** check "Initialize with README" (we'll upload files)
6. Click **"Create repository"**

### Step 3: Upload Backend Files to GitHub

#### Option A: Using GitHub Web Interface (Easiest)

1. After creating repository, you'll see "uploading an existing file"
2. Click **"uploading an existing file"**
3. Drag and drop these files from your `backend/` folder:
   - `server.py`
   - `start.py`
   - `database.py`
   - `config.py`
   - `user_api.py`
   - `product_api.py`
   - `cart_api.py`
   - `order_api.py`
   - `admin_api.py`
   - `staff_api.py`
   - `__init__.py`
   - `requirements.txt`
4. Scroll down, add commit message: `Initial backend upload`
5. Click **"Commit changes"**

#### Option B: Using Git Command Line (If you have Git installed)

1. Open terminal/command prompt in your `backend/` folder
2. Run these commands:

```bash
# Initialize git repository
git init

# Add all files
git add server.py start.py database.py config.py user_api.py product_api.py cart_api.py order_api.py admin_api.py staff_api.py __init__.py requirements.txt

# Commit
git commit -m "Initial backend upload"

# Add GitHub repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/chickenbites-backend.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Part 2: Deploy to Render

### Step 1: Create Render Account
1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with GitHub (recommended) or email
4. Verify your email

### Step 2: Connect GitHub to Render
1. In Render dashboard, click **"New +"** → **"Web Service"**
2. Click **"Connect GitHub"** (if not connected)
3. Authorize Render to access your GitHub
4. Select your repository: `chickenbites-backend`

### Step 3: Configure Web Service
Fill in these settings:

- **Name**: `chickenbites-api`
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `main` (or `master`)
- **Root Directory**: Leave empty (or `backend` if files are in subfolder)
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python start.py`

### Step 4: Set Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**

Add these one by one:

1. **Key**: `PORT` → **Value**: `8000`
2. **Key**: `DB_HOST` → **Value**: `srv2049.hstgr.io`
3. **Key**: `DB_NAME` → **Value**: `u761984878_csc4`
4. **Key**: `DB_USER` → **Value**: `u761984878_csc4`
5. **Key**: `DB_PASSWORD` → **Value**: `Azraelcisco123!`

### Step 5: Deploy
1. Scroll down and click **"Create Web Service"**
2. Render will start building (takes 2-5 minutes)
3. Watch the build logs - you'll see it installing dependencies
4. When done, you'll get a URL like: `https://chickenbites-api.onrender.com`

### Step 6: Test Your Backend
1. Copy your Render URL
2. Open in browser: `https://your-app-name.onrender.com/api/health`
3. You should see JSON response: `{"success": true, "status": "healthy", ...}`

## Part 3: Update Frontend

### Step 1: Update API URL
1. Open `frontend/api_client.py`
2. Find line with `API_BASE_URL`
3. Replace with your Render URL:

```python
API_BASE_URL = 'https://chickenbites-api.onrender.com'
```

(Use your actual Render URL)

### Step 2: Test Frontend
1. Run: `python main.py`
2. The frontend should connect to your Render backend
3. Backend connects to Hostinger database automatically

## Troubleshooting

### Build Fails
- Check build logs in Render dashboard
- Make sure `requirements.txt` has `mysql-connector-python==8.2.0`
- Check that all Python files are uploaded

### Database Connection Fails
- Verify environment variables are set correctly in Render
- Check Hostinger database allows remote connections
- Test database connection from Render logs

### API Not Responding
- Check Render service is running (not sleeping)
- Free tier services sleep after 15 min of inactivity
- First request after sleep takes ~30 seconds

## Summary

✅ **GitHub**: Backend code repository  
✅ **Render**: Backend server (runs automatically)  
✅ **Hostinger**: Database (stays there)  
✅ **Your Computer**: Frontend (connects to Render)

Everything is connected and working!

