"""Modern, zero-dependency web dashboard (Phase 1.6 Upgrade)."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


def generate_html(audit_file: Path) -> str:
    allowed, denied, held = 0, 0, 0
    rows = ""

    if audit_file.exists():
        with open(audit_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    action = data.get('action', '')
                    
                    if action == 'transfer_allowed': allowed += 1
                    elif action == 'transfer_denied': denied += 1
                    elif action == 'transfer_held': held += 1

                    badge_class = "allowed" if action == "transfer_allowed" else "denied" if action == "transfer_denied" else "held"
                    reason = data.get('reason', data.get('tx_hash', ''))
                    time_str = str(data.get('timestamp', ''))

                    rows += f"""
                    <tr>
                        <td><span class="badge {badge_class}">{action.replace('transfer_', '').upper()}</span></td>
                        <td class="mono">{time_str[:10]}</td>
                        <td class="mono truncate">{data.get('to', '')}</td>
                        <td class="mono">${data.get('amount_usd', '')}</td>
                        <td class="truncate">{reason}</td>
                    </tr>
                    """
                except Exception:
                    pass

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Zerix Dashboard</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg: #09090b;
                --card-bg: #18181b;
                --text: #f4f4f5;
                --text-muted: #a1a1aa;
                --accent: #3b82f6;
                --success: #10b981;
                --danger: #ef4444;
                --warning: #f59e0b;
                --border: #27272a;
            }}
            body {{
                font-family: 'Inter', sans-serif;
                background-color: var(--bg);
                color: var(--text);
                margin: 0;
                padding: 2rem;
                -webkit-font-smoothing: antialiased;
            }}
            .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }}
            h1 {{ margin: 0; font-weight: 600; font-size: 1.5rem; letter-spacing: -0.5px; }}
            .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 2rem; }}
            .stat-card {{ background: var(--card-bg); padding: 1.25rem; border-radius: 12px; border: 1px solid var(--border); }}
            .stat-title {{ color: var(--text-muted); font-size: 0.75rem; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 600; }}
            .stat-value {{ font-size: 2rem; font-weight: 600; }}
            .table-container {{ background: var(--card-bg); border-radius: 12px; border: 1px solid var(--border); overflow-x: auto; }}
            table {{ width: 100%; border-collapse: collapse; text-align: left; }}
            th {{ background: #18181b; padding: 1rem; color: var(--text-muted); font-weight: 500; font-size: 0.75rem; border-bottom: 1px solid var(--border); text-transform: uppercase; letter-spacing: 0.5px; }}
            td {{ padding: 1rem; border-bottom: 1px solid var(--border); font-size: 0.875rem; }}
            tr:last-child td {{ border-bottom: none; }}
            tr:hover {{ background: #1f1f22; }}
            .badge {{ padding: 0.25rem 0.75rem; border-radius: 999px; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.5px; }}
            .allowed {{ background: rgba(16, 185, 129, 0.15); color: var(--success); border: 1px solid rgba(16, 185, 129, 0.2); }}
            .denied {{ background: rgba(239, 68, 68, 0.15); color: var(--danger); border: 1px solid rgba(239, 68, 68, 0.2); }}
            .held {{ background: rgba(245, 158, 11, 0.15); color: var(--warning); border: 1px solid rgba(245, 158, 11, 0.2); }}
            .mono {{ font-family: 'JetBrains Mono', monospace; color: var(--text-muted); font-size: 0.8rem; }}
            .truncate {{ max-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
            .status-dot {{ display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: var(--success); margin-right: 8px; box-shadow: 0 0 10px var(--success); }}
            .header-badge {{ display: flex; align-items: center; font-size: 0.875rem; color: var(--text-muted); background: var(--card-bg); padding: 0.5rem 1rem; border-radius: 999px; border: 1px solid var(--border); }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Zerix Engine</h1>
            <div class="header-badge">
                <span class="status-dot"></span> System Online
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-title">Allowed</div>
                <div class="stat-value" style="color: var(--success);">{allowed}</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Denied</div>
                <div class="stat-value" style="color: var(--danger);">{denied}</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Held (HITL)</div>
                <div class="stat-value" style="color: var(--warning);">{held}</div>
            </div>
        </div>

        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Status</th>
                        <th>Timestamp</th>
                        <th>Recipient</th>
                        <th>Amount</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
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
    print(f"🚀 Modern Zerix Dashboard running at: http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
