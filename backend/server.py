"""
Simple Python HTTP Server for Chicken Bites Backend
Upload this to Hostinger - no Flask, no FastAPI, just pure Python
"""
import http.server
import socketserver
import json
import urllib.parse
from database import Database
from user_api import UserAPI
from product_api import ProductAPI
from cart_api import CartAPI
from order_api import OrderAPI
from admin_api import AdminAPI
from staff_api import StaffAPI

# Initialize database and APIs
db = Database()
user_api = UserAPI(db)
product_api = ProductAPI(db)
cart_api = CartAPI(db)
order_api = OrderAPI(db)
admin_api = AdminAPI(db)
staff_api = StaffAPI(db)

class APIHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def _send_json(self, data, status=200):
        """Send JSON response"""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _get_json_body(self):
        """Read JSON from request body"""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length)
        return json.loads(body.decode())
    
    def _get_query_params(self):
        """Parse query parameters"""
        if '?' in self.path:
            query_string = self.path.split('?')[1]
            return dict(urllib.parse.parse_qsl(query_string))
        return {}
    
    def do_GET(self):
        """Handle GET requests"""
        path = self.path.split('?')[0]
        params = self._get_query_params()
        
        try:
            # Health check
            if path == '/api/health':
                if db.connect():
                    db.disconnect()
                    self._send_json({'success': True, 'status': 'healthy', 'database': 'connected'})
                else:
                    self._send_json({'success': False, 'status': 'unhealthy', 'database': 'disconnected'}, 503)
                return
            
            # User endpoints
            if path.startswith('/api/user/'):
                user_id = int(path.split('/')[-1])
                user = user_api.get_user(user_id)
                if user:
                    user.pop('password', None)
                    self._send_json({'success': True, 'user': user})
                else:
                    self._send_json({'success': False, 'message': 'User not found'}, 404)
                return
            
            # Product endpoints
            if path == '/api/products':
                sort_by = params.get('sort_by', 'all')
                search = params.get('search', '')
                products = product_api.get_all_products(sort_by, search)
                self._send_json({'success': True, 'products': products})
                return
            
            if path.startswith('/api/products/') and path != '/api/products/categories' and not path.startswith('/api/products/category/'):
                product_id = int(path.split('/')[-1])
                product = product_api.get_product(product_id)
                if product:
                    self._send_json({'success': True, 'product': product})
                else:
                    self._send_json({'success': False, 'message': 'Product not found'}, 404)
                return
            
            if path == '/api/products/categories':
                categories = product_api.get_categories()
                self._send_json({'success': True, 'categories': categories})
                return
            
            if path.startswith('/api/products/category/'):
                category = path.split('/')[-1]
                products = product_api.get_products_by_category(category)
                self._send_json({'success': True, 'products': products})
                return
            
            # Cart endpoints
            if path.startswith('/api/cart/') and not path.endswith('/clear'):
                user_id = int(path.split('/')[-1])
                cart_items = cart_api.get_cart(user_id)
                total = cart_api.get_cart_total(user_id)
                self._send_json({'success': True, 'cart': cart_items, 'total': total})
                return
            
            # Order endpoints
            if path.startswith('/api/orders/'):
                parts = path.split('/')
                if path.endswith('/items'):
                    order_id = int(parts[-2])
                    items = order_api.get_order_items(order_id)
                    self._send_json({'success': True, 'items': items})
                elif not path.endswith('/status'):
                    # /api/orders/{user_id}
                    user_id = int(parts[-1])
                    status = params.get('status', 'all')
                    sort = params.get('sort', 'ASC')
                    orders = order_api.get_orders(user_id, status, sort)
                    self._send_json({'success': True, 'orders': orders})
                return
            
            # Admin endpoints
            if path == '/api/admin/dashboard/stats':
                stats = {
                    'pending_orders': admin_api.get_total_pending_orders(),
                    'total_orders': admin_api.get_total_orders(),
                    'completed_orders': admin_api.get_total_completed_orders(),
                    'total_products': admin_api.get_total_products(),
                    'total_users': admin_api.get_total_users(),
                    'total_admins': admin_api.get_total_admins(),
                    'total_staff': admin_api.get_total_staff()
                }
                self._send_json({'success': True, 'stats': stats})
                return
            
            if path == '/api/admin/products':
                sort_by = params.get('sort_by', 'all')
                search = params.get('search', '')
                products = admin_api.get_all_products(sort_by, search)
                self._send_json({'success': True, 'products': products})
                return
            
            if path == '/api/admin/orders':
                status = params.get('status', 'all')
                search = params.get('search', '')
                orders = admin_api.get_all_orders(status, search)
                self._send_json({'success': True, 'orders': orders})
                return
            
            if path == '/api/admin/users':
                user_type = params.get('type', 'all')
                sort_by = params.get('sort_by', 'newest')
                users = admin_api.get_all_users(user_type, sort_by)
                for user in users:
                    user.pop('password', None)
                self._send_json({'success': True, 'users': users})
                return
            
            # Staff endpoints
            if path == '/api/staff/dashboard/stats':
                stats = {
                    'pending_orders': staff_api.get_total_pending_orders(),
                    'total_orders': staff_api.get_total_orders(),
                    'completed_orders': staff_api.get_total_completed_orders(),
                    'completed_value': staff_api.get_total_completed_value(),
                    'total_products': staff_api.get_total_products()
                }
                self._send_json({'success': True, 'stats': stats})
                return
            
            if path == '/api/staff/orders':
                status = params.get('status', 'all')
                orders = staff_api.get_all_orders(status)
                self._send_json({'success': True, 'orders': orders})
                return
            
            if path == '/api/staff/products':
                sort_by = params.get('sort_by', 'all')
                search = params.get('search', '')
                products = staff_api.get_all_products(sort_by, search)
                self._send_json({'success': True, 'products': products})
                return
            
            self._send_json({'success': False, 'message': 'Not found'}, 404)
        except Exception as e:
            self._send_json({'success': False, 'message': str(e)}, 500)
    
    def do_POST(self):
        """Handle POST requests"""
        path = self.path.split('?')[0]
        data = self._get_json_body()
        
        try:
            # User endpoints
            if path == '/api/user/login':
                user = user_api.login(data.get('username'), data.get('password'))
                if user:
                    user.pop('password', None)
                    self._send_json({'success': True, 'user': user})
                else:
                    self._send_json({'success': False, 'message': 'Invalid credentials'}, 401)
                return
            
            if path == '/api/user/register':
                success, message = user_api.register(data)
                self._send_json({'success': success, 'message': message})
                return
            
            # Cart endpoints
            if path == '/api/cart':
                success, message = cart_api.add_to_cart(
                    data.get('user_id'),
                    data.get('product_id'),
                    data.get('quantity', 1),
                    data.get('product_data')
                )
                self._send_json({'success': success, 'message': message})
                return
            
            # Order endpoints
            if path == '/api/orders':
                success, message, order_id = order_api.create_order(
                    data.get('user_id'),
                    data.get('user_data'),
                    data.get('cart_items'),
                    data.get('payment_method')
                )
                self._send_json({'success': success, 'message': message, 'order_id': order_id})
                return
            
            # Admin endpoints
            if path == '/api/admin/products':
                success, message = admin_api.add_product(data)
                self._send_json({'success': success, 'message': message})
                return
            
            if path == '/api/admin/users':
                user_type = data.pop('user_type', 'client')
                success, message, user_id = admin_api.register_user(data, user_type)
                self._send_json({'success': success, 'message': message, 'user_id': user_id})
                return
            
            self._send_json({'success': False, 'message': 'Not found'}, 404)
        except Exception as e:
            self._send_json({'success': False, 'message': str(e)}, 500)
    
    def do_PUT(self):
        """Handle PUT requests"""
        path = self.path.split('?')[0]
        data = self._get_json_body()
        
        try:
            # User endpoints
            if path.endswith('/profile'):
                user_id = int(path.split('/')[-2])
                success, message = user_api.update_profile(user_id, data)
                self._send_json({'success': success, 'message': message})
                return
            
            if path.endswith('/address'):
                user_id = int(path.split('/')[-2])
                success, message = user_api.update_address(user_id, data.get('address'))
                self._send_json({'success': success, 'message': message})
                return
            
            if path.endswith('/username'):
                user_id = int(path.split('/')[-2])
                success, message = user_api.update_username(user_id, data.get('username'))
                self._send_json({'success': success, 'message': message})
                return
            
            # Cart endpoints
            if path.startswith('/api/cart/') and not path.endswith('/clear'):
                cart_id = int(path.split('/')[-1])
                success, message = cart_api.update_quantity(cart_id, data.get('quantity'))
                self._send_json({'success': success, 'message': message})
                return
            
            # Order endpoints
            if path.endswith('/status'):
                order_id = int(path.split('/')[-2])
                success, message = order_api.update_order_status(
                    order_id,
                    data.get('user_id'),
                    data.get('action')
                )
                self._send_json({'success': success, 'message': message})
                return
            
            # Admin endpoints
            if path.startswith('/api/admin/products/'):
                product_id = int(path.split('/')[-1])
                success, message = admin_api.update_product(product_id, data)
                self._send_json({'success': success, 'message': message})
                return
            
            if path.startswith('/api/admin/orders/'):
                order_id = int(path.split('/')[-1])
                success, message = admin_api.update_order_status(order_id, data.get('status'))
                self._send_json({'success': success, 'message': message})
                return
            
            if path.startswith('/api/admin/users/'):
                user_id = int(path.split('/')[-1])
                success, message = admin_api.update_user_info(user_id, data)
                self._send_json({'success': success, 'message': message})
                return
            
            # Staff endpoints
            if path.startswith('/api/staff/orders/'):
                order_id = int(path.split('/')[-1])
                success, message = staff_api.update_order_status(order_id, data.get('status'))
                self._send_json({'success': success, 'message': message})
                return
            
            if path.startswith('/api/staff/products/'):
                if path.endswith('/toggle-stock'):
                    product_id = int(path.split('/')[-2])
                    success, message = staff_api.toggle_stock_status(product_id)
                else:
                    product_id = int(path.split('/')[-1])
                    success, message = staff_api.update_product(product_id, data)
                self._send_json({'success': success, 'message': message})
                return
            
            self._send_json({'success': False, 'message': 'Not found'}, 404)
        except Exception as e:
            self._send_json({'success': False, 'message': str(e)}, 500)
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        path = self.path.split('?')[0]
        
        try:
            # Cart endpoints
            if path.startswith('/api/cart/'):
                if path.endswith('/clear'):
                    user_id = int(path.split('/')[-2])
                    success, message = cart_api.clear_cart(user_id)
                else:
                    cart_id = int(path.split('/')[-1])
                    success, message = cart_api.remove_item(cart_id)
                self._send_json({'success': success, 'message': message})
                return
            
            # Admin endpoints
            if path.startswith('/api/admin/products/'):
                product_id = int(path.split('/')[-1])
                success, message = admin_api.delete_product(product_id)
                self._send_json({'success': success, 'message': message})
                return
            
            if path.startswith('/api/admin/orders/'):
                order_id = int(path.split('/')[-1])
                success, message = admin_api.delete_order(order_id)
                self._send_json({'success': success, 'message': message})
                return
            
            if path.startswith('/api/admin/users/'):
                user_id = int(path.split('/')[-1])
                success, message = admin_api.delete_user(user_id)
                self._send_json({'success': success, 'message': message})
                return
            
            self._send_json({'success': False, 'message': 'Not found'}, 404)
        except Exception as e:
            self._send_json({'success': False, 'message': str(e)}, 500)

def run_server(port=8000):
    """Run the HTTP server"""
    import os
    # Get port from environment (Render provides this)
    port = int(os.getenv('PORT', port))
    db.connect()
    with socketserver.TCPServer(("0.0.0.0", port), APIHandler) as httpd:
        print(f"Server running on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    run_server(port)

