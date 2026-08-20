from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class YardSheetCreate(BaseModel):
    farm_id: int
    crop_name: str
    crop_variety: Optional[str] = None
    sowing_date: Optional[date] = None
    cultivated_area_acres: float = 1.0
    crop_stage: Optional[str] = "Vegetative"
    expected_yield_kg: Optional[float] = None
    season: Optional[str] = "Kharif"
    notes: Optional[str] = None

class YardSheetUpdate(BaseModel):
    crop_name: Optional[str] = None
    crop_variety: Optional[str] = None
    sowing_date: Optional[date] = None
    cultivated_area_acres: Optional[float] = None
    crop_stage: Optional[str] = None
    expected_yield_kg: Optional[float] = None
    actual_yield_kg: Optional[float] = None
    season: Optional[str] = None
    notes: Optional[str] = None

class YardSheetStageUpdate(BaseModel):
    crop_stage: str
    notes: Optional[str] = None
    actual_yield_kg: Optional[float] = None

class YardSheetResponse(BaseModel):
    id: int
    farm_id: int
    crop_name: str
    crop_variety: Optional[str] = None
    sowing_date: Optional[date] = None
    cultivated_area_acres: float
    crop_stage: str
    expected_yield_kg: Optional[float] = None
    actual_yield_kg: Optional[float] = None
    season: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
