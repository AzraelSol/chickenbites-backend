"""
Product API - handles product operations
"""
from .database import Database
from typing import Optional, List, Dict

class ProductAPI:
    def __init__(self, db: Database):
        self.db = db
    
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
    
    def get_products_by_category(self, category: str) -> List[Dict]:
        """Get products by category"""
        if category.lower() == 'all':
            return self.get_all_products()
        
        query = "SELECT * FROM products WHERE category = %s ORDER BY name"
        result = self.db.execute_query(query, (category,))
        return result if result else []
    
    def get_product(self, product_id: int) -> Optional[Dict]:
        """Get product by ID"""
        query = "SELECT * FROM products WHERE id = %s"
        result = self.db.execute_query(query, (product_id,))
        return result[0] if result and len(result) > 0 else None
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        query = "SELECT DISTINCT category FROM products WHERE category IS NOT NULL AND category != '' AND category != 'Out of stock' ORDER BY category"
        result = self.db.execute_query(query)
        if result:
            return [row['category'] for row in result]
        return []


