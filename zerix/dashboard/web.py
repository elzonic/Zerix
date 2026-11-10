"""Zero-dependency read-only web dashboard (Phase 1.6)."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

def generate_html(audit_file: Path) -> str:
    rows = ""
    if audit_file.exists():
        with open(audit_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    reason = data.get('reason', data.get('tx_hash', ''))
                    rows += f"<tr><td>{data.get('timestamp')}</td><td>{data.get('action')}</td><td>{data.get('to')}</td><td>${data.get('amount_usd')}</td><td>{reason}</td></tr>"
                except Exception:
                    pass

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Zerix Audit Dashboard</title>
        <style>
            body {{ font-family: monospace; padding: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h2>Zerix Audit Dashboard (Read-Only)</h2>
        <table>
            <tr><th>Timestamp</th><th>Action</th><th>To</th><th>Amount (USD)</th><th>Reason/TxHash</th></tr>
            {rows}
        </table>
    </body>
    </html>
    """

class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = generate_html(Path("audit.jsonl"))
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    def log_message(self, format, *args):
        pass

def run_dashboard(port: int = 8000) -> None:
    server = HTTPServer(('127.0.0.1', port), DashboardHandler)
    print(f"🚀 Zerix Dashboard running at: http://localhost:{port}")
    print("Tekan CTRL+C untuk mematikan server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMematikan server...")
        server.server_close()
