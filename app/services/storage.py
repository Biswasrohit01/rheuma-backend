"""Supabase Storage service for file uploads."""
import uuid
from datetime import datetime
from pathlib import Path
from app.core.config import settings
from app.core.database import get_db


async def upload_file_to_storage(
    file_content: bytes,
    file_name: str,
    content_type: str = "image/jpeg"
) -> str:
    """
    Upload a file to Supabase Storage and return the public URL.
    
    Args:
        file_content: Binary content of the file
        file_name: Original file name
        content_type: MIME type of the file
        
    Returns:
        Public URL of the uploaded file
        
    Raises:
        Exception: If upload fails
    """
    try:
        # Generate unique file name with timestamp and UUID
        file_extension = Path(file_name).suffix
        unique_file_name = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}{file_extension}"
        
        # Get Supabase client (synchronous, but we're in async function)
        supabase = get_db()
        bucket_name = settings.supabase_storage_bucket
        
        # Upload file to storage (synchronous operation in async function is fine)
        storage_response = supabase.storage.from_(bucket_name).upload(
            path=unique_file_name,
            file=file_content,
            file_options={
                "content-type": content_type,
                "upsert": False
            }
        )
        
        # Get public URL (synchronous operation)
        public_url = supabase.storage.from_(bucket_name).get_public_url(
            unique_file_name
        )
        
        return public_url
        
    except Exception as e:
        error_msg = str(e)
        # Provide more helpful error messages
        if "getaddrinfo failed" in error_msg or "11001" in error_msg:
            raise Exception(
                f"Network/DNS error: Cannot connect to Supabase. "
                f"Please check:\n"
                f"1. Your internet connection\n"
                f"2. Supabase URL in .env file: {settings.SUPABASE_URL}\n"
                f"3. If you're behind a firewall/proxy\n"
                f"4. Verify project exists at: https://supabase.com/dashboard"
            )
        raise Exception(f"Failed to upload file to storage: {error_msg}")