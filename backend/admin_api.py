"""
Admin API - handles admin operations
"""
from .database import Database
from typing import List, Dict, Optional, Tuple

class AdminAPI:
    def __init__(self, db: Database):
        self.db = db
    
    # Dashboard Stats
    def get_total_pending_orders(self) -> int:
        """Get total pending orders"""
        query = "SELECT COUNT(*) as total FROM orders WHERE payment_status = 'pending'"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_total_orders(self) -> int:
        """Get total orders"""
        query = "SELECT COUNT(*) as total FROM orders"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_total_completed_orders(self) -> int:
        """Get total completed orders"""
        query = "SELECT COUNT(*) as total FROM orders WHERE payment_status = 'completed_confirmed'"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_total_products(self) -> int:
        """Get total products"""
        query = "SELECT COUNT(*) as total FROM products"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_total_users(self) -> int:
        """Get total users (all types)"""
        query = "SELECT COUNT(*) as total FROM users"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_total_admins(self) -> int:
        """Get total admins"""
        query = "SELECT COUNT(*) as total FROM users WHERE user_type = 'admin'"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_total_staff(self) -> int:
        """Get total staff"""
        query = "SELECT COUNT(*) as total FROM users WHERE user_type = 'staff'"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    # Products Management
    def add_product(self, product_data: Dict) -> Tuple[bool, str]:
        """Add a new product"""
        # Check if product name already exists
        check_query = "SELECT * FROM products WHERE name = %s"
        existing = self.db.execute_query(check_query, (product_data['name'],))
        
        if existing and len(existing) > 0:
            return False, "Product name already exists!"
        
        insert_query = """
            INSERT INTO products (name, price, category, image, stock_status) 
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            product_data['name'],
            product_data['price'],
            product_data.get('category', ''),
            product_data.get('image', ''),
            product_data.get('stock_status', 'In stock')
        )
        
        if self.db.execute_update(insert_query, params):
            return True, "Product added successfully!"
        return False, "Failed to add product!"
    
    def update_product(self, product_id: int, product_data: Dict) -> Tuple[bool, str]:
        """Update a product"""
        import os
        import shutil
        
        # Handle image update if provided
        if 'image' in product_data and product_data['image']:
            try:
                # Get the source image path
                source_path = product_data['image']
                
                # Get just the filename
                image_filename = os.path.basename(source_path)
                
                # Determine upload directory (frontend/uploaded_img)
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                upload_dir = os.path.join(base_dir, 'frontend', 'uploaded_img')
                
                # Try alternative paths
                upload_paths = [
                    upload_dir,
                    os.path.join(base_dir, '..', 'frontend', 'uploaded_img'),
                    os.path.join('frontend', 'uploaded_img'),
                    os.path.join('..', 'frontend', 'uploaded_img')
                ]
                
                dest_dir = None
                for path in upload_paths:
                    if os.path.exists(path):
                        dest_dir = path
                        break
                
                if not dest_dir:
                    # Create directory if it doesn't exist
                    dest_dir = os.path.join(base_dir, 'frontend', 'uploaded_img')
                    os.makedirs(dest_dir, exist_ok=True)
                
                # Destination path
                destination_path = os.path.join(dest_dir, image_filename)
                
                # Copy image file
                if os.path.exists(source_path) and os.path.isfile(source_path):
                    shutil.copy(source_path, destination_path)
                    # Store relative path in database
                    db_image_path = image_filename
                else:
                    return False, "Image file not found!"
            except Exception as e:
                return False, f"Error uploading image: {str(e)}"
        else:
            # Get current image from database
            query = "SELECT image FROM products WHERE id = %s"
            result = self.db.execute_query(query, (product_id,))
            if result:
                db_image_path = result[0].get('image', '')
            else:
                db_image_path = ''
        
        # Build update query
        if 'image' in product_data and product_data['image']:
            update_query = """
                UPDATE products 
                SET name = %s, price = %s, category = %s, stock_status = %s, image = %s
                WHERE id = %s
            """
            params = (
                product_data['name'],
                product_data['price'],
                product_data.get('category', ''),
                product_data.get('stock_status', 'In stock'),
                db_image_path,
                product_id
            )
        else:
            update_query = """
                UPDATE products 
                SET name = %s, price = %s, category = %s, stock_status = %s
                WHERE id = %s
            """
            params = (
                product_data['name'],
                product_data['price'],
                product_data.get('category', ''),
                product_data.get('stock_status', 'In stock'),
                product_id
            )
        
        if self.db.execute_update(update_query, params):
            return True, "Product updated successfully!"
        return False, "Failed to update product!"
    
    def delete_product(self, product_id: int) -> Tuple[bool, str]:
        """Delete a product"""
        query = "DELETE FROM products WHERE id = %s"
        if self.db.execute_update(query, (product_id,)):
            return True, "Product deleted successfully!"
        return False, "Failed to delete product!"
    
    # Orders Management
    def get_all_orders(self, status_filter: str = 'all', search: str = '') -> List[Dict]:
        """Get all orders with optional filtering"""
        query = """
            SELECT orders.*, users.name, users.fname, users.mname, users.lname 
            FROM orders
            JOIN users ON orders.user_id = users.id
            WHERE 1=1
        """
        params = []
        
        if status_filter != 'all':
            query += " AND payment_status = %s"
            params.append(status_filter)
        
        if search:
            query += " AND (orders.id LIKE %s OR orders.name LIKE %s OR orders.email LIKE %s OR orders.oid LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param, search_param])
        
        query += " ORDER BY placed_on DESC"
        
        result = self.db.execute_query(query, tuple(params) if params else None)
        return result if result else []
    
    def update_order_status(self, order_id: int, status: str) -> Tuple[bool, str]:
        """Update order payment status"""
        # Map 'completed' to 'delivered' to match PHP behavior
        if status == 'completed':
            status = 'delivered'
        
        query = "UPDATE orders SET payment_status = %s WHERE id = %s"
        if self.db.execute_update(query, (status, order_id)):
            return True, "Order status updated successfully!"
        return False, "Failed to update order status!"
    
    def delete_order(self, order_id: int) -> Tuple[bool, str]:
        """Delete an order and its items"""
        try:
            # Delete order items first
            delete_items_query = "DELETE FROM order_items WHERE order_id = %s"
            self.db.execute_update(delete_items_query, (order_id,))
            
            # Delete order
            delete_order_query = "DELETE FROM orders WHERE id = %s"
            if self.db.execute_update(delete_order_query, (order_id,)):
                return True, "Order deleted successfully!"
            return False, "Failed to delete order!"
        except Exception as e:
            return False, f"Error deleting order: {str(e)}"
    
    # Users Management
    def get_all_users(self, user_type: str = 'all', sort_by: str = 'newest') -> List[Dict]:
        """Get all users, optionally filtered by type and sorted"""
        # Build base query
        if user_type == 'all':
            query = "SELECT * FROM users"
            params = []
        else:
            query = "SELECT * FROM users WHERE user_type = %s"
            params = [user_type]
        
        # Add sorting
        if sort_by == 'newest':
            query += " ORDER BY id DESC"
        elif sort_by == 'oldest':
            query += " ORDER BY id ASC"
        elif sort_by == 'name_asc':
            query += " ORDER BY name ASC"
        elif sort_by == 'name_desc':
            query += " ORDER BY name DESC"
        else:
            query += " ORDER BY id DESC"  # Default to newest
        
        result = self.db.execute_query(query, tuple(params) if params else None)
        return result if result else []
    
    def register_user(self, user_data: Dict, user_type: str = 'client') -> Tuple[bool, str, int]:
        """Register a new user (admin can create clients, admins, or staff)"""
        # Check if username or email already exists
        # Only check number if it's not empty
        check_conditions = ["name = %s", "email = %s"]
        check_params = [user_data['name'], user_data['email']]
        
        # Only check number if it's provided and not empty
        if user_data.get('number') and user_data['number'].strip():
            check_conditions.append("number = %s")
            check_params.append(user_data['number'].strip())
        
        check_query = f"""
            SELECT * FROM users 
            WHERE {' OR '.join(check_conditions)}
        """
        existing = self.db.execute_query(check_query, tuple(check_params))
        
        if existing and len(existing) > 0:
            # Check which field actually exists
            for user in existing:
                if user.get('name') == user_data['name']:
                    return False, "Username already exists!", 0
                if user.get('email') == user_data['email']:
                    return False, "Email already exists!", 0
                if user_data.get('number') and user_data['number'].strip() and user.get('number') == user_data['number'].strip():
                    return False, "Phone number already exists!", 0
            return False, "Username, email, or number already exists!", 0
        
        hashed_password = Database.hash_password(user_data['password'])
        insert_query = """
            INSERT INTO users 
            (name, fname, mname, lname, email, number, address, password, user_type) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            user_data['name'],
            user_data.get('fname', ''),
            user_data.get('mname', ''),
            user_data.get('lname', ''),
            user_data['email'],
            user_data['number'],
            user_data.get('address', ''),
            hashed_password,
            user_type
        )
        
        if self.db.execute_update(insert_query, params):
            # Get the inserted user ID
            get_id_query = "SELECT id FROM users WHERE name = %s AND email = %s ORDER BY id DESC LIMIT 1"
            result = self.db.execute_query(get_id_query, (user_data['name'], user_data['email']))
            user_id = result[0]['id'] if result else 0
            return True, f"{user_type.capitalize()} registered successfully!", user_id
        return False, f"Failed to register {user_type}!", 0
    
    def delete_user(self, user_id: int) -> Tuple[bool, str]:
        """Delete a user and all related records"""
        try:
            # Get all order IDs for this user first
            get_orders_query = "SELECT id FROM orders WHERE user_id = %s"
            orders = self.db.execute_query(get_orders_query, (user_id,))
            order_ids = [order['id'] for order in orders] if orders else []
            
            # Delete order items for this user's orders
            if order_ids:
                placeholders = ','.join(['%s'] * len(order_ids))
                delete_order_items_query = f"DELETE FROM order_items WHERE order_id IN ({placeholders})"
                self.db.execute_update(delete_order_items_query, tuple(order_ids))
            
            # Delete cart items
            delete_cart_query = "DELETE FROM cart WHERE user_id = %s"
            self.db.execute_update(delete_cart_query, (user_id,))
            
            # Delete orders for this user
            delete_orders_query = "DELETE FROM orders WHERE user_id = %s"
            self.db.execute_update(delete_orders_query, (user_id,))
            
            # Finally, delete the user
            delete_user_query = "DELETE FROM users WHERE id = %s"
            if self.db.execute_update(delete_user_query, (user_id,)):
                return True, "User deleted successfully!"
            return False, "Failed to delete user!"
        except Exception as e:
            return False, f"Error deleting user: {str(e)}"
    
    def update_user_info(self, user_id: int, user_data: Dict) -> Tuple[bool, str]:
        """Update user information"""
        # Build update query dynamically based on provided fields
        updates = []
        params = []
        
        if 'name' in user_data:
            # Check if username already exists
            check_query = "SELECT * FROM users WHERE name = %s AND id != %s"
            existing = self.db.execute_query(check_query, (user_data['name'], user_id))
            if existing and len(existing) > 0:
                return False, "Username already taken!"
            updates.append("name = %s")
            params.append(user_data['name'])
        
        if 'fname' in user_data:
            updates.append("fname = %s")
            params.append(user_data['fname'])
        
        if 'mname' in user_data:
            updates.append("mname = %s")
            params.append(user_data['mname'])
        
        if 'lname' in user_data:
            updates.append("lname = %s")
            params.append(user_data['lname'])
        
        if 'email' in user_data:
            updates.append("email = %s")
            params.append(user_data['email'])
        
        if 'number' in user_data:
            updates.append("number = %s")
            params.append(user_data['number'])
        
        if 'address' in user_data:
            updates.append("address = %s")
            params.append(user_data['address'])
        
        if 'profile_pic' in user_data:
            updates.append("profile_pic = %s")
            params.append(user_data['profile_pic'])
        
        if 'password' in user_data:
            # Hash password using SHA1 (matching PHP system)
            hashed_password = Database.hash_password(user_data['password'])
            updates.append("password = %s")
            params.append(hashed_password)
        
        if not updates:
            return False, "No fields to update!"
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        
        if self.db.execute_update(query, tuple(params)):
            return True, "User information updated successfully!"
        return False, "Failed to update user information!"

