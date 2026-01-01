import asyncio
from supabase import create_client
from app.core.config import settings

# Create a fresh, dedicated client for storage
# This prevents the "coroutine" error by bypassing the shared connection
storage_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

async def upload_file_to_storage(file_content: bytes, file_name: str, content_type: str) -> str:
    try:
        bucket_name = "scans"
        
        # 1. Upload the file (Supabase Python client is synchronous)
        res = storage_client.storage.from_(bucket_name).upload(
            path=file_name,
            file=file_content,
            file_options={"content-type": content_type, "upsert": "true"}
        )

        # 2. Get the public URL
        # The .get_public_url() method returns a string directly in newer versions
        public_url = storage_client.storage.from_(bucket_name).get_public_url(file_name)
        
        return public_url

    except Exception as e:
        # If it fails, we will know exactly why
        raise Exception(f"Storage Upload Failed: {str(e)}")