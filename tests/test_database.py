"""Unit tests for SQLite Database and Auth (Phase 3.2)."""

import os
from zerix.database import init_db, create_user, get_user_by_api_key, generate_api_key
from zerix.database.models import DB_PATH

def test_database_flow(tmp_path):
    # Override DB_PATH for testing
    import zerix.database.models
    original_path = zerix.database.models.DB_PATH
    zerix.database.models.DB_PATH = tmp_path / "test.db"

    init_db()
    
    # 1. Generate API Key and Create User
    api_key = generate_api_key()
    assert api_key.startswith("zx_")
    
    success = create_user("test@zerix.com", api_key, role="admin")
    assert success is True
    
    # 2. Try duplicate email (should fail gracefully)
    assert create_user("test@zerix.com", generate_api_key()) is False
    
    # 3. Retrieve User via API Key (Auth Simulation)
    user = get_user_by_api_key(api_key)
    assert user is not None
    assert user["email"] == "test@zerix.com"
    assert user["role"] == "admin"
    
    # 4. Invalid API Key
    assert get_user_by_api_key("zx_invalid_key") is None

    # Restore DB_PATH
    zerix.database.models.DB_PATH = original_path
