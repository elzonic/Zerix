import json
from zerix.dashboard.web import generate_html

def test_generate_html_empty(tmp_path):
    log_file = tmp_path / "audit.jsonl"
    html = generate_html(log_file)
    assert "Zerix Audit Dashboard" in html

def test_generate_html_with_data(tmp_path):
    log_file = tmp_path / "audit.jsonl"
    with open(log_file, "w") as f:
        f.write(json.dumps({"timestamp": 123456789, "action": "transfer_allowed", "to": "0xabc", "amount_usd": "5.00", "tx_hash": "0xmock_123"}) + "\n")
    html = generate_html(log_file)
    assert "0xabc" in html
    assert "0xmock_123" in html
