from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CropRecommendationRequest(BaseModel):
    farm_id: Optional[int] = None
    soil_type: Optional[str] = "Black Soil"
    soil_ph: Optional[float] = 6.8
    nitrogen_n: Optional[float] = 70.0
    phosphorus_p: Optional[float] = 35.0
    potassium_k: Optional[float] = 45.0
    temperature: Optional[float] = 27.0
    humidity: Optional[float] = 65.0
    rainfall: Optional[float] = 800.0
    water_availability: Optional[str] = "Moderate"
    farm_size_acres: Optional[float] = 2.0
    season: Optional[str] = "Kharif"
    state: Optional[str] = "Gujarat"

class CropRecommendationItem(BaseModel):
    crop_name: str
    suitability_score: float
    confidence_level: str  # High, Moderate, Good
    reason: str
    water_requirement: str
    fertilizer_advice: str
    basic_requirements: str
    potential_risks: str
    expected_yield_range: str
    market_outlook: str

class CropRecommendationResponse(BaseModel):
    farm_id: Optional[int] = None
    analysis_date: datetime
    environmental_summary: dict
    recommendations: List[CropRecommendationItem]
