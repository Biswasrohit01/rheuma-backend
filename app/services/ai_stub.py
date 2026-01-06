"""AI analysis stub service (mocks Azure analysis)."""
import asyncio
from typing import Dict, Any
from datetime import datetime


async def analyze_scan(image_url: str) -> Dict[str, Any]:
    """
    Mock AI analysis function that simulates Azure analysis.
    
    Args:
        image_url: URL of the image to analyze
        
    Returns:
        Dictionary containing mock analysis results
    """
    # Simulate processing time (2 seconds)
    await asyncio.sleep(2)
    
    # Return dummy analysis results
    return {
        "confidence": 0.85,
        "diagnosis": "Rheumatoid Arthritis",
        "severity": "Moderate",
        "affected_joints": ["wrist", "finger"],
        "analysis_date": datetime.utcnow().isoformat(),
        "image_url": image_url,
        "recommendations": [
            "Follow up with rheumatologist",
            "Consider anti-inflammatory medication",
            "Monitor joint mobility"
        ]
    }






