"""
Staff API - handles staff operations
"""
from .database import Database
from typing import List, Dict, Optional, Tuple

class StaffAPI:
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
    
    def get_total_completed_value(self) -> float:
        """Get total value of completed orders (payment_status = 'completed')"""
        query = "SELECT SUM(total_price) as total FROM orders WHERE payment_status = 'completed'"
        result = self.db.execute_query(query)
        return float(result[0]['total']) if result and result[0]['total'] else 0.0
    
    def get_total_products(self) -> int:
        """Get total products count"""
        query = "SELECT COUNT(*) as total FROM products"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    def get_total_completed_orders(self) -> int:
        """Get total completed orders"""
        query = "SELECT COUNT(*) as total FROM orders WHERE payment_status = 'completed_confirmed'"
        result = self.db.execute_query(query)
        return result[0]['total'] if result else 0
    
    # Orders Management (Staff can view and update orders)
    def get_all_orders(self, status_filter: str = 'all') -> List[Dict]:
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
    
    # Products (Staff can view and update products, but not delete)
    def get_all_products(self, sort_by: str = 'all', search: str = '') -> List[Dict]:
        """Get all products with optional sorting and search"""
        query = "SELECT * FROM products"
        params = []
        
        # Add search condition
        if search:
            query += " WHERE name LIKE %s"
            params.append(f'%{search}%')
        
        # Add sorting
        if sort_by == 'all':
            # Show all products, grouped by category then newest first
            query += " ORDER BY category ASC, id DESC"
        elif sort_by == 'newest':
            query += " ORDER BY id DESC"
        elif sort_by == 'oldest':
            query += " ORDER BY id ASC"
        elif sort_by == 'affordable':
            if search:
                query += " AND category = 'Affordable'"
            else:
                query += " WHERE category = 'Affordable'"
            query += " ORDER BY id DESC"
        elif sort_by == 'best_seller':
            if search:
                query += " AND category = 'Best seller'"
            else:
                query += " WHERE category = 'Best seller'"
            query += " ORDER BY id DESC"
        elif sort_by == 'combo_meal':
            if search:
                query += " AND category = 'Combo meal'"
            else:
                query += " WHERE category = 'Combo meal'"
            query += " ORDER BY id DESC"
        else:
            query += " ORDER BY id DESC"  # Default to newest
        
        result = self.db.execute_query(query, tuple(params) if params else None)
        return result if result else []
    
    def update_product(self, product_id: int, product_data: Dict) -> Tuple[bool, str]:
        """Update a product (staff can update but not delete)"""
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
    
    def toggle_stock_status(self, product_id: int) -> Tuple[bool, str]:
        """Toggle product stock status between 'In stock' and 'Out of stock'"""
        # Get current stock status
        query = "SELECT stock_status FROM products WHERE id = %s"
        result = self.db.execute_query(query, (product_id,))
        
        if not result:
            return False, "Product not found!"
        
        current_status = result[0]['stock_status']
        new_status = 'Out of stock' if current_status == 'In stock' else 'In stock'
        
        # Update stock status
        update_query = "UPDATE products SET stock_status = %s WHERE id = %s"
        if self.db.execute_update(update_query, (new_status, product_id)):
            return True, f"Stock status changed to '{new_status}'!"
        return False, "Failed to update stock status!"


