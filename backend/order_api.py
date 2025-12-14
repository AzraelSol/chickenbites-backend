"""
Order API - handles order operations
"""
from .database import Database
from typing import List, Dict, Optional
import random
import string
from datetime import datetime

class OrderAPI:
    def __init__(self, db: Database):
        self.db = db
    
    def generate_order_id(self, length: int = 10) -> str:
        """Generate random order ID"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def create_order(self, user_id: int, user_data: Dict, cart_items: List[Dict], payment_method: str) -> tuple[bool, str, Optional[str]]:
        """Create a new order from cart items"""
        try:
            # Calculate totals
            total_products = sum(item['quantity'] for item in cart_items)
            total_price = sum(item['price'] * item['quantity'] for item in cart_items)
            
            # Generate order ID
            oid = self.generate_order_id()
            
            # Insert order (matching PHP system's checkout.php structure)
            order_query = """
                INSERT INTO orders 
                (user_id, oid, name, number, email, method, address, total_products, total_price, placed_on, payment_status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, 'pending')
            """
            order_params = (
                user_id,
                oid,
                user_data['name'],
                user_data['number'],
                user_data['email'],
                payment_method,
                user_data['address'],
                total_products,
                total_price
            )
            
            if not self.db.execute_update(order_query, order_params):
                return False, "Failed to create order!", None
            
            # Get order ID
            order_id = self.db.get_last_insert_id()
            if not order_id:
                return False, "Failed to get order ID!", None
            
            # Insert order items
            for item in cart_items:
                item_query = """
                    INSERT INTO order_items (order_id, product_name, quantity) 
                    VALUES (%s, %s, %s)
                """
                if not self.db.execute_update(item_query, (order_id, item['name'], item['quantity'])):
                    return False, "Failed to add order items!", None
            
            # Clear cart
            clear_query = "DELETE FROM cart WHERE user_id = %s"
            if not self.db.execute_update(clear_query, (user_id,)):
                return False, "Order created but failed to clear cart!", oid
            
            return True, "Order placed successfully!", oid
            
        except Exception as e:
            return False, f"Error creating order: {str(e)}", None
    
    def get_orders(self, user_id: int, status_filter: str = 'all', sort_order: str = 'ASC') -> List[Dict]:
        """Get orders for user"""
        query = """
            SELECT orders.*, users.name, CONCAT(users.fname, ' ', users.mname, ' ', users.lname) AS full_name 
            FROM orders
            JOIN users ON orders.user_id = users.id
            WHERE orders.user_id = %s
        """
        params = [user_id]
        
        if status_filter != 'all':
            if status_filter == 'confirmed':
                query += " AND (payment_status = 'confirmed' OR payment_status = 'completed_confirmed')"
            else:
                query += " AND payment_status = %s"
                params.append(status_filter)
        
        # Add ordering
        if sort_order == 'DESC':
            query += " ORDER BY placed_on DESC"
        else:
            query += " ORDER BY placed_on ASC"
        
        result = self.db.execute_query(query, tuple(params))
        return result if result else []
    
    def get_order_items(self, order_id: int) -> List[Dict]:
        """Get items for an order"""
        query = """
            SELECT order_items.product_name, order_items.quantity, products.price 
            FROM order_items 
            JOIN products ON order_items.product_name = products.name 
            WHERE order_items.order_id = %s
        """
        result = self.db.execute_query(query, (order_id,))
        return result if result else []
    
    def update_order_status(self, order_id: str, user_id: int, action: str) -> tuple[bool, str]:
        """Update order status (cancel, confirm, etc.)"""
        if action == 'cancel':
            query = "UPDATE orders SET payment_status = 'cancelled' WHERE oid = %s AND user_id = %s"
        elif action == 'confirm':
            query = """
                UPDATE orders SET payment_status = CASE 
                    WHEN payment_status = 'delivered' THEN 'completed_confirmed' 
                    ELSE 'confirmed' 
                END 
                WHERE oid = %s AND user_id = %s
            """
        elif action == 'confirm_delivery':
            query = "UPDATE orders SET payment_status = 'delivered' WHERE oid = %s AND user_id = %s"
        else:
            return False, "Invalid action!"
        
        if self.db.execute_update(query, (order_id, user_id)):
            return True, "Order status updated!"
        return False, "Failed to update order status!"


