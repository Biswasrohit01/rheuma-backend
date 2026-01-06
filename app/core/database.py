"""Supabase database client initialization."""
from supabase import create_client, Client
from app.core.config import settings
import sys

# Initialize the client globally ONCE
try:
    _db_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
except Exception as e:
    error_msg = str(e)
    if "getaddrinfo failed" in error_msg or "11001" in error_msg:
        print("\n" + "="*60)
        print("ERROR: Cannot connect to Supabase!")
        print("="*60)
        print(f"URL: {settings.SUPABASE_URL}")
        print("\nPossible issues:")
        print("1. Check your internet connection")
        print("2. Verify Supabase URL is correct")
        print("3. Check if project exists: https://supabase.com/dashboard")
        print("4. Check firewall/proxy settings")
        print("5. Try: ping supabase.co")
        print("="*60 + "\n")
    raise

def get_db() -> Client:
    """
    Returns the Supabase client.
    This is NOT async, to prevent 'coroutine' errors.
    """
    return _db_client