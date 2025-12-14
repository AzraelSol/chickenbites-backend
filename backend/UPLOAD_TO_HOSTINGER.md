# Upload Backend to Hostinger - Simple Guide

## What to Upload

Upload these files to your Hostinger public_html folder (or a subfolder like `api/`):

1. `server.py` - Main server file
2. `start.py` - Startup script
3. `database.py` - Database connection
4. `config.py` - Configuration
5. `user_api.py` - User API
6. `product_api.py` - Product API
7. `cart_api.py` - Cart API
8. `order_api.py` - Order API
9. `admin_api.py` - Admin API
10. `staff_api.py` - Staff API
11. `requirements.txt` - Dependencies

## Steps

1. **Upload all files** to Hostinger (via FTP or File Manager)

2. **Install Python dependencies** on Hostinger:
   ```bash
   pip install mysql-connector-python
   ```

3. **Update config.py** with your Hostinger database credentials:
   - Set `DB_HOST` to `localhost` (when running on Hostinger)
   - Set your database name, user, and password

4. **Run the server**:
   ```bash
   python start.py
   ```
   
   Or specify a port:
   ```bash
   python start.py 8000
   ```

5. **Update frontend API URL** in `frontend/api_client.py`:
   - Change `API_BASE_URL` to your Hostinger URL where the server is running
   - Example: `http://yourdomain.com:8000` or `http://yourdomain.com/api`

## Note

- The server uses Python's built-in HTTP server (no Flask, no FastAPI)
- Make sure Python 3 is installed on your Hostinger server
- The server will run on port 8000 by default (or the port you specify)
- Keep the server running (use `nohup` or a process manager if needed)

