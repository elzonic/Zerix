"""Web server and API for the modern Zerix Dashboard."""

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. API Endpoint: Mengambil data audit terbaru
        if self.path == '/api/audit':
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
            
            # Return the last 50 transactions
            self.wfile.write(json.dumps(data[-50:]).encode('utf-8'))
            return

        # 2. Serve Static Files (HTML, CSS)
        if self.path == '/' or self.path == '/index.html':
            filepath = 'web/index.html'
            content_type = 'text/html'
        elif self.path == '/dashboard.html':
            filepath = 'web/dashboard.html'
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

    def log_message(self, format, *args):
        # Mute HTTP logs
        pass


def run_dashboard(port: int = 8000) -> None:
    # Pastikan server dijalankan dari root folder proyek
    os.chdir(Path(__file__).parent.parent.parent)
    
    server = HTTPServer(('127.0.0.1', port), DashboardHandler)
    print(f"🚀 Zerix Live Dashboard running at: http://localhost:{port}/dashboard.html")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMematikan server...")
        server.server_close()
