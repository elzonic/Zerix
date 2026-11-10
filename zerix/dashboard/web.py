"""Web server and API for the modern Zerix SaaS Dashboard."""

import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.cookies import SimpleCookie
from pathlib import Path

from zerix.database import (
    init_db, create_user, get_user_by_api_key, 
    create_api_key, get_api_keys, delete_api_key,
    create_session, get_user_by_session, delete_session
)

class DashboardHandler(BaseHTTPRequestHandler):
    def _get_session_token(self):
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            cookie = SimpleCookie(cookie_header)
            if 'zerix_session' in cookie:
                return cookie['zerix_session'].value
        return None

    def _get_user(self):
        token = self._get_session_token()
        if token:
            user = get_user_by_session(token)
            if user: return user
        api_key = self.headers.get('X-API-Key')
        if api_key:
            return get_user_by_api_key(api_key)
        return None

    def _set_cookie(self, token: str):
        self.send_header('Set-Cookie', f'zerix_session={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=604800')

    def do_GET(self):
        if self.path == '/api/me':
            user = self._get_user()
            if user:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(user).encode('utf-8'))
            else:
                self.send_response(401); self.end_headers()
            return

        if self.path == '/api/audit':
            user = self._get_user()
            if not user:
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
        if self.path == '/api/register':
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            email = data.get('email')
            
            if create_user(email):
                api_key = create_api_key(email)
                session_token = create_session(email)
                
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self._set_cookie(session_token)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "api_key": api_key}).encode('utf-8'))
            else:
                self.send_response(409); self.end_headers()
                self.wfile.write(json.dumps({"error": "Email already registered"}).encode('utf-8'))
            return

        if self.path == '/api/login':
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            api_key = data.get('api_key')
            
            user = get_user_by_api_key(api_key)
            if user:
                session_token = create_session(user["email"])
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self._set_cookie(session_token)
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "email": user["email"]}).encode('utf-8'))
            else:
                self.send_response(401); self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid API Key"}).encode('utf-8'))
            return
            
        if self.path == '/api/logout':
            token = self._get_session_token()
            if token: delete_session(token)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Set-Cookie', 'zerix_session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "logged_out"}).encode('utf-8'))
            return

        if self.path == '/api/keys':
            user = self._get_user()
            if not user: self.send_response(401); self.end_headers(); return
            new_key = create_api_key(user["email"])
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"api_key": new_key}).encode('utf-8'))
            return

        if self.path == '/api/approve':
            user = self._get_user()
            if not user: self.send_response(401); self.end_headers(); return
            
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
        if self.path == '/api/keys':
            user = self._get_user()
            if not user: self.send_response(401); self.end_headers(); return
                
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            
            if delete_api_key(user["email"], data.get('api_key')):
                self.send_response(200); self.end_headers()
                self.wfile.write(json.dumps({"status": "deleted"}).encode('utf-8'))
            else:
                # Jika gagal (karena key terakhir), kirim 400 Bad Request dengan JSON error
                self.send_response(400); self.end_headers()
                self.wfile.write(json.dumps({"error": "Cannot delete the last API key."}).encode('utf-8'))
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
