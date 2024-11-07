import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer

# Configure logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def log_request_id(self, request_id):
        """Log value of X-Request-ID"""
        if request_id:
            logger.info(f"Received X-Request-ID: {request_id}")
        else:
            logger.info("No X-Request-ID found in the request")

    def do_GET(self):
        """GET-request handler"""
        if self.path == "/api/v1/hello":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            request_id = self.headers.get('X-Request-ID', None)
            self.log_request_id(request_id)

            response = {
                "success": True,
                "X-Request-ID": request_id,
                "data": {
                    "message": "Hello, World!"
                }
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """POST-request handler"""
        if self.path == "/api/v1/greet":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_id = self.headers.get('X-Request-ID', None)
            self.log_request_id(request_id)

            try:
                data = json.loads(post_data.decode('utf-8'))
                name = data.get("name", "stranger")

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                response = {
                    "success": True,
                    "X-Request-ID": request_id,
                    "data": {
                        "message": f"Hello, {name}!"
                    }
                }
                self.wfile.write(json.dumps(response).encode('utf-8'))
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid JSON"}')
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=SimpleAPIHandler, port=3000):
    """Launch server on 3000 port"""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
