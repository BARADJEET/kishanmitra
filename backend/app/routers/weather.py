from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User
from ..models.farm import Farm
from ..services.auth_service import get_current_user
from ..services.weather_advisory_engine import get_weather_and_advisory

router = APIRouter(prefix="/api/weather", tags=["Weather Advisory"])

@router.get("/current")
async def get_current_weather(
    lat: float = Query(23.0225, description="Latitude"),
    lon: float = Query(72.5714, description="Longitude"),
    district: str = Query("Ahmedabad", description="District name"),
    current_user: User = Depends(get_current_user)
):
    return await get_weather_and_advisory(lat=lat, lon=lon, district=district)

@router.get("/farm/{farm_id}")
async def get_farm_weather(
    farm_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    lat = farm.latitude if farm and farm.latitude else 23.0225
    lon = farm.longitude if farm and farm.longitude else 72.5714
    district = farm.district if farm else "Ahmedabad"
    return await get_weather_and_advisory(lat=lat, lon=lon, district=district)
