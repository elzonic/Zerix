"""Web server and API for the modern Zerix SaaS Dashboard."""

import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from zerix.database import init_db, create_user, get_user_by_api_key, generate_api_key

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Protected API Endpoint: Mengambil data audit
        if self.path == '/api/audit':
            # Cek API Key dari Header
            api_key = self.headers.get('X-API-Key')
            user = get_user_by_api_key(api_key) if api_key else None
            
            # Untuk demo lokal, kita izinkan jika belum ada user (mode dev)
            # Di production, baris ini harus dihapus (wajib login)
            if not user and api_key != "dev_mode":
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Unauthorized. Invalid or missing X-API-Key."}).encode('utf-8'))
                return

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            audit_file = Path("audit.jsonl")
            data = []
            if audit_file.exists():
                with open(audit_file, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            data.append(json.loads(line))
                        except json.JSONDecodeError:
                            pass
            
            self.wfile.write(json.dumps(data[-50:]).encode('utf-8'))
            return

        # 2. Serve Static Files
        if self.path == '/' or self.path == '/index.html':
            filepath = 'web/index.html'
            content_type = 'text/html'
        elif self.path == '/dashboard.html':
            filepath = 'web/dashboard.html'
            content_type = 'text/html'
        elif self.path == '/login.html':
            filepath = 'web/login.html'
            content_type = 'text/html'
        elif self.path == '/login.html':
            filepath = 'web/login.html'
            content_type = 'text/html'
        elif self.path == '/style.css':
            filepath = 'web/style.css'
            content_type = 'text/css'
        else:
            self.send_response(404)
            self.end_headers()
            return

        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        # 1. API Endpoint Registrasi (Mendapatkan API Key)
        if self.path == '/api/register':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            email = data.get('email')
            if not email:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Email is required"}).encode('utf-8'))
                return
                
            # Generate API Key dan Simpan ke Database
            api_key = generate_api_key()
            success = create_user(email=email, api_key=api_key, role="admin")
            
            if success:
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "api_key": api_key}).encode('utf-8'))
            else:
                self.send_response(409) # Conflict (Email sudah terdaftar)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Email already registered"}).encode('utf-8'))
            return

        # 2. API Endpoint HITL Approval
        if self.path == '/api/approve':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            original_ts = data.get('timestamp')
            
            if original_ts:
                approval_log = {
                    "timestamp": time.time(),
                    "action": "transfer_allowed",
                    "original_timestamp": original_ts,
                    "to": "Approved by Human",
                    "amount_usd": "0.00",
                    "tx_hash": f"0xhuman_approved_{int(time.time())}"
                }
                with open("audit.jsonl", "a", encoding="utf-8") as f:
                    f.write(json.dumps(approval_log) + "\n")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            else:
                self.send_response(400)
                self.end_headers()
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        pass


def run_dashboard(port: int = 8000) -> None:
    os.chdir(Path(__file__).parent.parent.parent)
    init_db() # Pastikan tabel database siap saat server menyala
    server = HTTPServer(('127.0.0.1', port), DashboardHandler)
    print(f"🚀 Zerix SaaS API running at: http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMematikan server...")
        server.server_close()
