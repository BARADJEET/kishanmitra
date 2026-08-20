from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.farm import Farm, SoilRecord
from ..schemas.farm_schema import FarmCreate, FarmUpdate, FarmResponse, SoilRecordCreate, SoilRecordResponse
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/api/farms", tags=["Farm Management"])

@router.get("/", response_model=List[FarmResponse])
def get_farmer_farms(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == "admin":
        return db.query(Farm).all()
    return db.query(Farm).filter(Farm.farmer_id == current_user.id).all()

@router.post("/", response_model=FarmResponse, status_code=status.HTTP_201_CREATED)
def create_farm(farm_in: FarmCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_farm = Farm(
        farmer_id=current_user.id,
        farm_name=farm_in.farm_name,
        land_area_acres=farm_in.land_area_acres,
        state=farm_in.state,
        district=farm_in.district,
        village=farm_in.village,
        latitude=farm_in.latitude or 23.0225,
        longitude=farm_in.longitude or 72.5714,
        soil_type=farm_in.soil_type,
        irrigation_type=farm_in.irrigation_type,
        water_availability=farm_in.water_availability
    )
    db.add(new_farm)
    db.commit()
    db.refresh(new_farm)

    if farm_in.initial_soil:
        soil = SoilRecord(
            farm_id=new_farm.id,
            nitrogen_n=farm_in.initial_soil.nitrogen_n,
            phosphorus_p=farm_in.initial_soil.phosphorus_p,
            potassium_k=farm_in.initial_soil.potassium_k,
            soil_ph=farm_in.initial_soil.soil_ph,
            organic_carbon=farm_in.initial_soil.organic_carbon,
            notes=farm_in.initial_soil.notes
        )
        db.add(soil)
        db.commit()
        db.refresh(new_farm)

    return new_farm

@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm_by_id(farm_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    if current_user.role != "admin" and farm.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return farm

@router.put("/{farm_id}", response_model=FarmResponse)
def update_farm(farm_id: int, farm_in: FarmUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    if current_user.role != "admin" and farm.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    for field, val in farm_in.model_dump(exclude_unset=True).items():
        setattr(farm, field, val)
    db.commit()
    db.refresh(farm)
    return farm

@router.delete("/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_farm(farm_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    if current_user.role != "admin" and farm.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    db.delete(farm)
    db.commit()
    return None

@router.post("/{farm_id}/soil", response_model=SoilRecordResponse)
def add_soil_record(farm_id: int, soil_in: SoilRecordCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    farm = db.query(Farm).filter(Farm.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    if current_user.role != "admin" and farm.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    soil = SoilRecord(farm_id=farm.id, **soil_in.model_dump())
    db.add(soil)
    db.commit()
    db.refresh(soil)
    return soil
