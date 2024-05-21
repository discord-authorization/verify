import json
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

OAUTH2_CLIENT_ID = '1242183096804053003'
OAUTH2_CLIENT_SECRET = 'xOifdVdR2AdyEbKNgIwhBJqxrYKa07ny'
TOKEN_URL = 'https://discord.com/api/oauth2/token'

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open('index.html', 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        code = data['code']

        token_data = self.exchange_code_for_token(code)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(token_data).encode('utf-8'))

        print("User authorized. Token data:")
        print(token_data)

    def exchange_code_for_token(self, code):
        data = {
            'client_id': OAUTH2_CLIENT_ID,
            'client_secret': OAUTH2_CLIENT_SECRET,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'https://discord-authorization.github.io/verify/'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(TOKEN_URL, data=data, headers=headers)
        return response.json()

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
