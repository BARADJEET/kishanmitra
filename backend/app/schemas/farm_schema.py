from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class SoilRecordCreate(BaseModel):
    nitrogen_n: float = 60.0
    phosphorus_p: float = 30.0
    potassium_k: float = 40.0
    soil_ph: float = 6.5
    organic_carbon: Optional[float] = 0.6
    notes: Optional[str] = None

class SoilRecordResponse(SoilRecordCreate):
    id: int
    farm_id: int
    test_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class FarmCreate(BaseModel):
    farm_name: str
    land_area_acres: float = 1.0
    state: str = "Gujarat"
    district: str = "Ahmedabad"
    village: Optional[str] = None
    latitude: Optional[float] = 23.0225
    longitude: Optional[float] = 72.5714
    soil_type: str = "Black Soil"
    irrigation_type: str = "Drip"
    water_availability: str = "Moderate"
    initial_soil: Optional[SoilRecordCreate] = None

class FarmUpdate(BaseModel):
    farm_name: Optional[str] = None
    land_area_acres: Optional[float] = None
    state: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    soil_type: Optional[str] = None
    irrigation_type: Optional[str] = None
    water_availability: Optional[str] = None

class FarmResponse(BaseModel):
    id: int
    farmer_id: int
    farm_name: str
    land_area_acres: float
    state: str
    district: str
    village: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    soil_type: str
    irrigation_type: str
    water_availability: str
    created_at: datetime
    updated_at: datetime
    soil_records: List[SoilRecordResponse] = []

    class Config:
        from_attributes = True
