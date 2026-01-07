"""Pydantic models for request/response schemas."""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class ScanCreate(BaseModel):
    """Schema for creating a new scan."""
    
    patient_name: str = Field(..., min_length=1, max_length=255, description="Patient's full name")
    age: int = Field(..., ge=0, le=150, description="Patient's age")
    
    @field_validator('patient_name')
    @classmethod
    def validate_patient_name(cls, v: str) -> str:
        """Validate and sanitize patient name."""
        return v.strip()
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "patient_name": "John Doe",
                "age": 45
            }
        }


class ScanResponse(BaseModel):
    """Schema for scan response."""
    
    id: str = Field(..., description="Scan ID")
    patient_name: str = Field(..., description="Patient's full name")
    age: int = Field(..., description="Patient's age")
    image_url: str = Field(..., description="Public URL of the uploaded scan image")
    analysis_result: Dict[str, Any] = Field(..., description="AI analysis results")
    created_at: datetime = Field(..., description="Scan creation timestamp")
    
    class Config:
        """Pydantic config."""
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "patient_name": "John Doe",
                "age": 45,
                "image_url": "https://supabase.co/storage/v1/object/public/scans/scan_123.jpg",
                "analysis_result": {
                    "confidence": 0.85,
                    "diagnosis": "Rheumatoid Arthritis",
                    "severity": "Moderate"
                },
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


class PatientData(BaseModel):
    """Schema for patient data in upload request."""
    
    patient_name: str = Field(..., min_length=1, max_length=255, description="Patient's full name")
    age: int = Field(..., ge=0, le=150, description="Patient's age")
    
    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "patient_name": "John Doe",
                "age": 45
            }
        }

