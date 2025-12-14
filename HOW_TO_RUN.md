# How to Run Backend on Hostinger

## Method 1: Using SSH (Recommended if you have SSH access)

1. **Connect to Hostinger via SSH**
   - Use an SSH client (PuTTY, Terminal, etc.)
   - Connect to your Hostinger server

2. **Navigate to your backend folder**
   ```bash
   cd public_html/api
   # or wherever you uploaded the backend files
   ```

3. **Install dependencies**
   ```bash
   pip3 install mysql-connector-python
   ```

4. **Update config.py**
   - Edit `config.py` and set `DB_HOST` to `localhost`
   - Update database credentials

5. **Run the server**
   ```bash
   python3 start.py
   ```
   
   **OR run in background (keeps running after you disconnect):**
   ```bash
   nohup python3 start.py > server.log 2>&1 &
   ```

6. **Check if it's running**
   ```bash
   ps aux | grep python
   ```

## Method 2: Using Hostinger Python App (If Available)

1. **Login to Hostinger hPanel**
2. **Go to "Python App" or "Applications"**
3. **Create New Python App**
   - App name: `chickenbites-api`
   - Python version: 3.x
   - Startup file: `start.py`
   - App directory: `/public_html/api` (or your backend folder)
4. **Install dependencies** (in Python App settings)
   - Add: `mysql-connector-python`
5. **Start the app**

## Method 3: Using .htaccess (For Apache/PHP hosting)

If you can't run Python directly, you might need to use a different approach. However, the simple HTTP server won't work with .htaccess alone.

## Important Notes:

- **Port**: The server runs on port 8000 by default
- **Hostinger shared hosting**: May not allow custom ports
- **Solution**: You might need to use Hostinger's Python App feature or a VPS

## Check if Server is Running:

Test in browser or terminal:
```bash
curl http://csc4.gisrabies.com:8000/api/health
```

Or visit in browser:
```
http://csc4.gisrabies.com:8000/api/health
```

## Troubleshooting:

- **"Port already in use"**: Another process is using port 8000
- **"Permission denied"**: You don't have permission to bind to that port
- **"Cannot connect"**: Server isn't running or firewall is blocking

## Alternative: Use Different Port

Edit `start.py` to use a different port:
```python
port = int(os.getenv('PORT', 8080))  # Try 8080 instead of 8000
```

