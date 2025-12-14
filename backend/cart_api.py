"""
Cart API - handles shopping cart operations
"""
from .database import Database
from typing import List, Dict, Optional

class CartAPI:
    def __init__(self, db: Database):
        self.db = db
    
    def add_to_cart(self, user_id: int, product_id: int, quantity: int, product_data: Dict) -> tuple[bool, str]:
        """Add product to cart"""
        # Check if item already in cart
        check_query = "SELECT * FROM cart WHERE user_id = %s AND pid = %s"
        existing = self.db.execute_query(check_query, (user_id, product_id))
        
        if existing and len(existing) > 0:
            # Update quantity
            new_quantity = existing[0]['quantity'] + quantity
            update_query = "UPDATE cart SET quantity = %s WHERE user_id = %s AND pid = %s"
            if self.db.execute_update(update_query, (new_quantity, user_id, product_id)):
                return True, "Cart updated!"
            return False, "Failed to update cart!"
        else:
            # Insert new item
            insert_query = """
                INSERT INTO cart (user_id, pid, name, price, quantity, image) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                user_id,
                product_id,
                product_data['name'],
                product_data['price'],
                quantity,
                product_data['image']
            )
            if self.db.execute_update(insert_query, params):
                return True, "Added to cart!"
            return False, "Failed to add to cart!"
    
    def get_cart(self, user_id: int) -> List[Dict]:
        """Get all cart items for user"""
        query = "SELECT * FROM cart WHERE user_id = %s"
        result = self.db.execute_query(query, (user_id,))
        return result if result else []
    
    def update_quantity(self, cart_id: int, quantity: int) -> tuple[bool, str]:
        """Update cart item quantity"""
        query = "UPDATE cart SET quantity = %s WHERE id = %s"
        if self.db.execute_update(query, (quantity, cart_id)):
            return True, "Quantity updated!"
        return False, "Failed to update quantity!"
    
    def remove_item(self, cart_id: int) -> tuple[bool, str]:
        """Remove item from cart"""
        query = "DELETE FROM cart WHERE id = %s"
        if self.db.execute_update(query, (cart_id,)):
            return True, "Item removed!"
        return False, "Failed to remove item!"
    
    def clear_cart(self, user_id: int) -> tuple[bool, str]:
        """Clear all items from cart"""
        query = "DELETE FROM cart WHERE user_id = %s"
        if self.db.execute_update(query, (user_id,)):
            return True, "Cart cleared!"
        return False, "Failed to clear cart!"
    
    def get_cart_total(self, user_id: int) -> float:
        """Calculate cart total"""
        cart_items = self.get_cart(user_id)
        total = 0
        for item in cart_items:
            total += item['price'] * item['quantity']
        return total


