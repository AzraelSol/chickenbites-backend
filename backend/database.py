"""
Database connection and configuration

This module connects to the same database as the main PHP system.
Database: chickenbites
Host: localhost
User: root
Password: (empty)

This ensures both the tkinter desktop app and the main web system share the same data.
"""
import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, List, Tuple
import hashlib

class Database:
    def __init__(self):
        # Database configuration - supports both local and Hostinger deployment
        # Use environment variables for Hostinger, fallback to config or local defaults
        import os
        try:
            # Try to import config from backend folder
            from .config import DB_CONFIG
            self.host = os.getenv('DB_HOST', DB_CONFIG.get('host', 'localhost'))
            self.port = int(os.getenv('DB_PORT', DB_CONFIG.get('port', 3306)))
            self.database = os.getenv('DB_NAME', DB_CONFIG.get('database', 'chickenbites'))
            self.user = os.getenv('DB_USER', DB_CONFIG.get('user', 'root'))
            self.password = os.getenv('DB_PASSWORD', DB_CONFIG.get('password', ''))
        except ImportError:
            # Fallback to environment variables or defaults
            self.host = os.getenv('DB_HOST', 'localhost')
            self.port = int(os.getenv('DB_PORT', 3306))
            self.database = os.getenv('DB_NAME', 'chickenbites')
            self.user = os.getenv('DB_USER', 'root')
            self.password = os.getenv('DB_PASSWORD', '')
        self.connection: Optional[mysql.connector.MySQLConnection] = None
    
    def connect(self) -> bool:
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                connection_timeout=10,
                autocommit=True
            )
            return True
        except Error as e:
            error_msg = str(e)
            print(f"Error connecting to database: {error_msg}")
            print(f"Connection details: host={self.host}, port={self.port}, database={self.database}, user={self.user}")
            return False
        except Exception as e:
            error_msg = str(e)
            print(f"Unexpected error connecting to database: {error_msg}")
            print(f"Connection details: host={self.host}, port={self.port}, database={self.database}, user={self.user}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def execute_query(self, query: str, params: Tuple = None) -> Optional[List[Dict]]:
        """Execute SELECT query and return results"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            print(f"Error executing query: {e}")
            return None
    
    def execute_update(self, query: str, params: Tuple = None) -> bool:
        """Execute INSERT/UPDATE/DELETE query"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
            
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error executing update: {e}")
            if self.connection:
                self.connection.rollback()
            return False
    
    def get_last_insert_id(self) -> Optional[int]:
        """Get last inserted ID"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else None
        except Error as e:
            print(f"Error getting last insert ID: {e}")
            return None
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA1 (matching PHP sha1)"""
        return hashlib.sha1(password.encode()).hexdigest()


