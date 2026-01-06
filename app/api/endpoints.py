from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import ScanResponse
from app.services.storage import upload_file_to_storage
from supabase import create_client
from app.core.config import settings
import json

# --- THIS IS THE LINE YOU ASKED ABOUT ---
from app.services.ai_stub import analyze_scan 
# ----------------------------------------

router = APIRouter(prefix="/api/v1", tags=["scans"])

# Create a fresh DB connection (Fixes the "Coroutine" Error 500)
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

@router.post("/upload", response_model=ScanResponse)
async def upload_scan(
    file: UploadFile = File(...),
    patient_data: str = Form(...)
):
    try:
        print("1. Starting Upload...")
        
        # 1. Parse Data
        try:
            p_data = json.loads(patient_data)
        except:
            raise HTTPException(400, "Invalid JSON in patient_data")

        # 2. Upload to Storage
        print("2. Uploading file...")
        content = await file.read()
        file_url = await upload_file_to_storage(content, file.filename, file.content_type)
        print(f"   -> File URL: {file_url}")

        # 3. Azure AI Analysis
        print("3. Calling Azure AI...")
        analysis = await analyze_scan(file_url)
        print(f"   -> AI Result: {analysis}")

        # 4. Save to Database (Synchronous - Fixes crash)
        print("4. Saving to DB...")
        data = {
            "patient_name": p_data.get("patient_name", "Unknown"),
            "age": p_data.get("age", 0),
            "file_url": file_url,
            "analysis": analysis
        }
        
        response = supabase.table("scans").insert(data).execute()
        
        # 5. Success!
        record = response.data[0]
        print("✅ Success! Scan saved.")

        return {
            "id": record["id"],
            "patient_name": record["patient_name"],
            "age": record["age"],
            "image_url": record["file_url"],
            "analysis_result": record["analysis"],
            "created_at": record["created_at"]
        }

    except Exception as e:
        print(f"🔥 ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))