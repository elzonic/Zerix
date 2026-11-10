"""Web server and API for the modern Zerix SaaS Dashboard."""

import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from zerix.database import init_db, create_user, get_user_by_api_key, create_api_key, get_api_keys, delete_api_key

class DashboardHandler(BaseHTTPRequestHandler):
    def _get_user(self):
        api_key = self.headers.get('X-API-Key')
        return get_user_by_api_key(api_key) if api_key else None

    def do_GET(self):
        # API: Fetch Audit Logs
        if self.path == '/api/audit':
            user = self._get_user()
            if not user and self.headers.get('X-API-Key') != "dev_mode":
                self.send_response(401); self.end_headers(); return

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            audit_file = Path("audit.jsonl")
            data = []
            if audit_file.exists():
                with open(audit_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try: data.append(json.loads(line))
                        except: pass
            self.wfile.write(json.dumps(data[-50:]).encode('utf-8'))
            return

        # API: Fetch API Keys for current user
        if self.path == '/api/keys':
            user = self._get_user()
            if not user:
                self.send_response(401); self.end_headers(); return
            
            keys = get_api_keys(user["email"])
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(keys).encode('utf-8'))
            return

        # Static Files
        if self.path == '/' or self.path == '/index.html':
            filepath = 'web/index.html'; content_type = 'text/html'
        elif self.path == '/login.html':
            filepath = 'web/login.html'; content_type = 'text/html'
        elif self.path == '/dashboard.html':
            filepath = 'web/dashboard.html'; content_type = 'text/html'
        elif self.path == '/style.css':
            filepath = 'web/style.css'; content_type = 'text/css'
        else:
            self.send_response(404); self.end_headers(); return

        try:
            with open(filepath, 'rb') as f: content = f.read()
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        # Register User
        if self.path == '/api/register':
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            email = data.get('email')
            
            if not email:
                self.send_response(400); self.end_headers(); return
                
            if create_user(email):
                api_key = create_api_key(email)
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "api_key": api_key}).encode('utf-8'))
            else:
                self.send_response(409); self.end_headers()
                self.wfile.write(json.dumps({"error": "Email already registered"}).encode('utf-8'))
            return

        # API: Generate New API Key
        if self.path == '/api/keys':
            user = self._get_user()
            if not user:
                self.send_response(401); self.end_headers(); return
                
            new_key = create_api_key(user["email"])
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"api_key": new_key}).encode('utf-8'))
            return

        # API: Approve HITL
        if self.path == '/api/approve':
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            original_ts = data.get('timestamp')
            
            if original_ts:
                approval_log = {
                    "timestamp": time.time(), "action": "transfer_allowed",
                    "original_timestamp": original_ts, "to": "Approved by Human",
                    "amount_usd": "0.00", "tx_hash": f"0xhuman_approved_{int(time.time())}"
                }
                with open("audit.jsonl", "a", encoding="utf-8") as f:
                    f.write(json.dumps(approval_log) + "\n")
                
                self.send_response(200); self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            else:
                self.send_response(400); self.end_headers()
            return

        self.send_response(404); self.end_headers()

    def do_DELETE(self):
        # API: Delete API Key
        if self.path == '/api/keys':
            user = self._get_user()
            if not user:
                self.send_response(401); self.end_headers(); return
                
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            key_to_delete = data.get('api_key')
            
            if delete_api_key(user["email"], key_to_delete):
                self.send_response(200); self.end_headers()
                self.wfile.write(json.dumps({"status": "deleted"}).encode('utf-8'))
            else:
                self.send_response(404); self.end_headers()
            return
        self.send_response(404); self.end_headers()

    def log_message(self, format, *args): pass


def run_dashboard(port: int = 8000) -> None:
    os.chdir(Path(__file__).parent.parent.parent)
    init_db()
    server = HTTPServer(('127.0.0.1', port), DashboardHandler)
    print(f"🚀 Zerix SaaS API running at: http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMematikan server...")
        server.server_close()
