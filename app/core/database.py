"""Supabase database client initialization."""
from typing import Optional
from supabase import create_async_client, AsyncClient
from app.core.config import settings


class Database:
    """Database client singleton."""
    
    _client: Optional[AsyncClient] = None
    
    @classmethod
    def get_client(cls) -> AsyncClient:
        """Get or create Supabase async client instance."""
        if cls._client is None:
            cls._client = create_async_client(
                settings.supabase_url,
                settings.supabase_key
            )
        return cls._client
    
    @classmethod
    def reset_client(cls) -> None:
        """Reset client instance (useful for testing)."""
        cls._client = None


# Convenience function to get database client
def get_db() -> AsyncClient:
    """Get Supabase async database client."""
    return Database.get_client()

