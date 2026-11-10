"""Authentication utilities."""

import secrets

def generate_api_key() -> str:
    """Generates a secure, URL-safe API key for users."""
    return f"zx_{secrets.token_urlsafe(32)}"
