# Hostinger Backend Setup Guide

## Important: Hostinger Shared Hosting Limitations

On Hostinger shared hosting, you **cannot** run a Python HTTP server directly on port 80. You need to set it up differently.

## Option 1: Use a Subdirectory (Recommended)

1. Upload all backend files to a subdirectory on Hostinger, e.g., `public_html/api/`

2. Update `frontend/api_client.py`:
   ```python
   API_BASE_URL = 'http://csc4.gisrabies.com/api'
   ```

3. Create `.htaccess` in the `api/` folder:
   ```apache
   RewriteEngine On
   RewriteCond %{REQUEST_FILENAME} !-f
   RewriteCond %{REQUEST_FILENAME} !-d
   RewriteRule ^(.*)$ server.py/$1 [QSA,L]
   ```

## Option 2: Use Hostinger Python App (If Available)

1. In Hostinger hPanel, go to Python App
2. Create a new Python app
3. Point it to your backend folder
4. Set startup file to `start.py`
5. Use the provided domain/URL

## Option 3: Use CGI (Alternative)

Convert `server.py` to use CGI instead of HTTP server, or use a different approach.

## Current Issue

The error "Cannot connect to API server" means:
- The Python server isn't running on Hostinger, OR
- The URL path is incorrect, OR  
- The server isn't accessible via HTTP

**Check:**
1. Is the backend uploaded to Hostinger?
2. Is `python start.py` running on Hostinger?
3. What's the exact path where backend files are located?
4. Try accessing `http://csc4.gisrabies.com/api/health` in a browser to test

