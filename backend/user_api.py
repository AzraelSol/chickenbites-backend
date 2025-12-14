"""
User API - handles user authentication and profile management
"""
from .database import Database
from typing import Optional, Dict

class UserAPI:
    def __init__(self, db: Database):
        self.db = db
    
    def login(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user and return user data"""
        hashed_password = Database.hash_password(password)
        
        # Check for admin or staff
        query = """
            SELECT * FROM users 
            WHERE name = %s AND password = %s 
            AND (user_type = 'admin' OR user_type = 'staff')
        """
        result = self.db.execute_query(query, (username, hashed_password))
        
        if result and len(result) > 0:
            return result[0]
        
        # Check for client
        query = """
            SELECT * FROM users 
            WHERE name = %s AND password = %s 
            AND user_type = 'client'
        """
        result = self.db.execute_query(query, (username, hashed_password))
        
        if result and len(result) > 0:
            return result[0]
        
        return None
    
    def register(self, user_data: Dict) -> tuple[bool, str]:
        """Register a new user (client only)"""
        # Check if email, number, or address already exists
        check_query = """
            SELECT * FROM users 
            WHERE email = %s OR number = %s OR address = %s
        """
        existing = self.db.execute_query(
            check_query, 
            (user_data['email'], user_data['number'], user_data['address'])
        )
        
        if existing and len(existing) > 0:
            return False, "Email, number or address already exists!"
        
        # Check password match
        if user_data['password'] != user_data['cpassword']:
            return False, "Passwords do not match!"
        
        # Insert new user
        hashed_password = Database.hash_password(user_data['password'])
        insert_query = """
            INSERT INTO users 
            (name, fname, mname, lname, email, number, address, password, user_type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'client')
        """
        
        params = (
            user_data['name'],
            user_data['fname'],
            user_data['mname'],
            user_data['lname'],
            user_data['email'],
            user_data['number'],
            user_data['address'],
            hashed_password
        )
        
        if self.db.execute_update(insert_query, params):
            return True, "Registration successful!"
        else:
            return False, "Registration failed!"
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        query = "SELECT * FROM users WHERE id = %s"
        result = self.db.execute_query(query, (user_id,))
        return result[0] if result and len(result) > 0 else None
    
    def update_profile(self, user_id: int, user_data: Dict) -> tuple[bool, str]:
        """Update user profile"""
        query = """
            UPDATE users 
            SET fname = %s, mname = %s, lname = %s, 
                email = %s, number = %s 
            WHERE id = %s
        """
        params = (
            user_data['fname'],
            user_data['mname'],
            user_data['lname'],
            user_data['email'],
            user_data['number'],
            user_id
        )
        
        if self.db.execute_update(query, params):
            return True, "Profile updated successfully!"
        else:
            return False, "Failed to update profile!"
    
    def update_address(self, user_id: int, address: str) -> tuple[bool, str]:
        """Update user address"""
        query = "UPDATE users SET address = %s WHERE id = %s"
        if self.db.execute_update(query, (address, user_id)):
            return True, "Address updated successfully!"
        else:
            return False, "Failed to update address!"
    
    def update_profile_picture(self, user_id: int, profile_pic: str) -> tuple[bool, str]:
        """Update user profile picture (filename only)"""
        query = "UPDATE users SET profile_pic = %s WHERE id = %s"
        if self.db.execute_update(query, (profile_pic, user_id)):
            return True, "Profile picture updated successfully!"
        else:
            return False, "Failed to update profile picture!"
    
    def update_username(self, user_id: int, username: str) -> tuple[bool, str]:
        """Update username"""
        # Check if username already exists
        check_query = "SELECT * FROM users WHERE name = %s AND id != %s"
        existing = self.db.execute_query(check_query, (username, user_id))
        
        if existing and len(existing) > 0:
            return False, "Username already taken!"
        
        query = "UPDATE users SET name = %s WHERE id = %s"
        if self.db.execute_update(query, (username, user_id)):
            return True, "Username updated successfully!"
        else:
            return False, "Failed to update username!"


