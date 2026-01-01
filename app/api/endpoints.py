"""API endpoints for RheumaLens."""
from typing import List
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse
from app.models.schemas import ScanCreate, ScanResponse, PatientData
from app.services.storage import upload_file_to_storage
from app.services.ai_stub import analyze_scan
from app.core.database import get_db
import json


router = APIRouter(prefix="/api/v1", tags=["scans"])


@router.post(
    "/upload",
    response_model=ScanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload scan image and process with AI",
    description="Accepts an image file and patient data, uploads to storage, processes with AI, and saves to database"
)
async def upload_scan(
    file: UploadFile = File(..., description="Scan image file"),
    patient_data: str = Form(..., description="JSON string containing patient_name and age")
) -> ScanResponse:
    """
    Upload a scan image and process it.
    """
    try:
        # 1. Parse patient data
        try:
            patient_dict = json.loads(patient_data)
            patient = PatientData(**patient_dict)
        except (json.JSONDecodeError, ValueError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid patient_data JSON: {str(e)}"
            )
        
        # 2. Validate file type
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        # 3. Read file content
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty"
            )
        
        # 4. Upload file to Supabase Storage
        # NOTE: If this fails, we might need to remove 'await' here too, 
        # but let's try keeping it first as your storage function might be async.
        file_url = await upload_file_to_storage(
            file_content=file_content,
            file_name=file.filename or "scan.jpg",
            content_type=file.content_type
        )
        
        # 5. Analyze scan with AI stub
        analysis_result = await analyze_scan(image_url=file_url)
        
        # 6. Save to database
        supabase = get_db()
        
        scan_data = {
            "patient_name": patient.patient_name,
            "age": patient.age,
            "file_url": file_url,
            "analysis": analysis_result
        }
        
        # --- CRITICAL FIX: REMOVED 'await' HERE ---
        # Supabase client is synchronous. Putting 'await' here causes Error 500.
        db_response = supabase.table("scans").insert(scan_data).execute()
        
        if not db_response.data or len(db_response.data) == 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save scan to database"
            )
        
        # 7. Convert database response to ScanResponse
        scan_record = db_response.data[0]
        
        return ScanResponse(
            id=scan_record["id"],
            patient_name=scan_record["patient_name"],
            age=scan_record["age"],
            image_url=scan_record["file_url"],
            analysis_result=scan_record["analysis"],
            created_at=scan_record["created_at"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # This will print the exact error to your terminal if it fails again
        print(f"CRITICAL ERROR IN UPLOAD: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )


@router.get(
    "/patients",
    response_model=List[ScanResponse],
    summary="Get all patient scans",
    description="Fetches all scans from the database ordered by creation date (newest first)"
)
async def get_patients() -> List[ScanResponse]:
    """
    Get all patient scans ordered by date.
    """
    try:
        supabase = get_db()
        
        # --- CRITICAL FIX: REMOVED 'await' HERE TOO ---
        response = supabase.table("scans").select("*").order("created_at", desc=True).execute()
        
        if not response.data:
            return []
        
        # Convert to ScanResponse models
        scans = [
            ScanResponse(
                id=scan["id"],
                patient_name=scan["patient_name"],
                age=scan["age"],
                image_url=scan["file_url"],
                analysis_result=scan["analysis"],
                created_at=scan["created_at"]
            )
            for scan in response.data
        ]
        
        return scans
        
    except Exception as e:
        print(f"CRITICAL ERROR IN GET: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch scans: {str(e)}"
        )
        