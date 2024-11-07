import json
import logging
import uuid
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

# Registered email <-> userId storage
registered_accounts = dict()

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def log_request_id(self, request_id):
        """Log value of X-Request-ID"""
        if request_id:
            logger.info(f"Received X-Request-ID: {request_id}")
        else:
            logger.info("No X-Request-ID found in the request")

    def do_GET(self):
        """GET-request handler"""
        request_id = self.headers.get('X-Request-ID', None)
        self.log_request_id(request_id)

        if self.path == "/api/v1/hello":
            self.handle_hello_request(request_id)
        elif re.match(r"/api/v1/profile\?userId=[a-f0-9\-]{36}", self.path):
            self.handle_get_profile_request(request_id)
        else:
            self.send_not_found(request_id)

    def do_POST(self):
        """POST-request handler"""
        request_id = self.headers.get('X-Request-ID', None)
        self.log_request_id(request_id)

        if self.path == "/api/v1/greet":
            self.handle_greet_request(request_id)
        elif self.path == "/api/v1/register":
            self.handle_register_request(request_id)
        else:
            self.send_not_found(request_id)

    def handle_hello_request(self, request_id):
        """Hello request handler"""
        response = {
            "success": True,
            "data": {
                "message": "Hello, World!"
            }
        }
        self.send_status_headers_response(200, request_id, response)

    def handle_get_profile_request(self, request_id):
        """Get profile request handler"""
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)
        user_id = query_params.get('userId', [None])[0]
        email = find_key_by_value(registered_accounts, user_id)
        if email:
            response = {
                "success": True,
                "data": {
                    "userId": user_id,
                    "email": email
                }
            }
            self.send_status_headers_response(200, request_id, response)
        else:
           response = {
               "success": False,
               "data": {
                   "message": f"User account {user_id} not found."
               }
           }
           self.send_status_headers_response(200, request_id, response)

    def handle_register_request(self, request_id):
        """Register request handler"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode('utf-8'))
            email = data.get("email", "")

            if not email.strip():
                response = {
                    "success": False,
                    "data": {
                        "error": "Empty email"
                    }
                }
                self.send_status_headers_response(400, request_id, response)
            else:
                userId = str(uuid.uuid4())
                registered_accounts[email] = userId

                response = {
                    "success": True,
                    "data": {
                        "email": email,
                        "userId": userId,
                        "message": "Account successfully registered."
                    }
                }
                self.send_status_headers_response(200, request_id, response)
        except json.JSONDecodeError:
            self.send_invalid_json_response(request_id)
        logger.info(f"Registered accounts: {registered_accounts}")

    def handle_greet_request(self, request_id):
        """Greeting request handler"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data.decode('utf-8'))
            name = data.get("name", "stranger")

            response = {
                "success": True,
                "data": {
                    "message": f"Hello, {name}!"
                }
            }
            self.send_status_headers_response(200, request_id, response)
        except json.JSONDecodeError:
            self.send_invalid_json_response(request_id)

    def send_not_found(self, request_id):
        self.send_response(404)
        self.send_header("X-Request-ID", request_id)
        self.end_headers()

    def send_status_headers_response(self, status, request_id, response):
        self.send_response(status)
        self.send_header("X-Request-ID", request_id)
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def send_invalid_json_response(self, request_id):
        response = {
            "success": False,
            "data": {
                "error": "Invalid JSON"
            }
        }
        self.send_status_headers_response(400, request_id, response)

def run(server_class=HTTPServer, handler_class=SimpleAPIHandler, port=3000):
    """Launch server on 3000 port"""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    logger.info(f"Registered accounts: {registered_accounts}")
    httpd.serve_forever()

def find_key_by_value(d, value):
    for key, val in d.items():
        if val == value:
            return key
    return None

if __name__ == '__main__':
    run()
