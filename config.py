"""
Configuration file for Hostinger deployment
Your Hostinger database credentials are configured here
"""
import os

# Database Configuration
# For desktop app (running locally): use remote database host 'srv2049.hstgr.io'
# For web server (running on Hostinger): use 'localhost'
# 
# Remote MySQL hostname from Hostinger: srv2049.hstgr.io (or IP: 148.222.53.11)
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'srv2049.hstgr.io'),  # Remote MySQL hostname from Hostinger
    'port': int(os.getenv('DB_PORT', '3306')),  # MySQL default port
    'database': os.getenv('DB_NAME', 'u761984878_csc4'),
    'user': os.getenv('DB_USER', 'u761984878_csc4'),
    'password': os.getenv('DB_PASSWORD', 'Azraelcisco123!')
}
# Note: Set these as environment variables in Render dashboard

# API Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'https://srv2049-files.hstgr.io/46316da882db1028/files/public_html/csc4/')

# Flask Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'production')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Note: For production, it's recommended to use environment variables
# instead of hardcoded values. Set these in Hostinger hPanel:
# - DB_HOST=localhost (use 'localhost' when app runs on Hostinger server)
# - DB_NAME=u761984878_csc4
# - DB_USER=u761984878_csc4
# - DB_PASSWORD=Azraelcisco123!
#
# phpMyAdmin URL: https://auth-db2049.hstgr.io/index.php?route=/database/structure&db=u761984878_csc4
# (This is for database management, not the connection host)

