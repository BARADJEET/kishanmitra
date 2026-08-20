from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.farm import Farm
from ..models.yard_sheet import YardSheet
from ..schemas.yard_sheet_schema import YardSheetCreate, YardSheetUpdate, YardSheetResponse, YardSheetStageUpdate
from ..services.auth_service import get_current_user

router = APIRouter(prefix="/api/yard-sheets", tags=["Digital Yard Sheet"])

@router.get("/", response_model=List[YardSheetResponse])
def get_yard_sheets(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == "admin":
        return db.query(YardSheet).all()
    
    # Get all yard sheets for this farmer's farms
    farmer_farm_ids = [f.id for f in current_user.farms]
    return db.query(YardSheet).filter(YardSheet.farm_id.in_(farmer_farm_ids)).all()

@router.post("/", response_model=YardSheetResponse, status_code=status.HTTP_201_CREATED)
def create_yard_sheet(sheet_in: YardSheetCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    farm = db.query(Farm).filter(Farm.id == sheet_in.farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")
    if current_user.role != "admin" and farm.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this farm")

    new_sheet = YardSheet(**sheet_in.model_dump())
    db.add(new_sheet)
    db.commit()
    db.refresh(new_sheet)
    return new_sheet

@router.get("/{sheet_id}", response_model=YardSheetResponse)
def get_yard_sheet(sheet_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sheet = db.query(YardSheet).filter(YardSheet.id == sheet_id).first()
    if not sheet:
        raise HTTPException(status_code=404, detail="Yard sheet record not found")
    if current_user.role != "admin" and sheet.farm.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return sheet

@router.put("/{sheet_id}", response_model=YardSheetResponse)
def update_yard_sheet(sheet_id: int, sheet_in: YardSheetUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sheet = db.query(YardSheet).filter(YardSheet.id == sheet_id).first()
    if not sheet:
        raise HTTPException(status_code=404, detail="Yard sheet record not found")
    if current_user.role != "admin" and sheet.farm.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    for field, val in sheet_in.model_dump(exclude_unset=True).items():
        setattr(sheet, field, val)
    db.commit()
    db.refresh(sheet)
    return sheet

@router.patch("/{sheet_id}/stage", response_model=YardSheetResponse)
def update_crop_stage(sheet_id: int, stage_in: YardSheetStageUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sheet = db.query(YardSheet).filter(YardSheet.id == sheet_id).first()
    if not sheet:
        raise HTTPException(status_code=404, detail="Yard sheet not found")
    if current_user.role != "admin" and sheet.farm.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    sheet.crop_stage = stage_in.crop_stage
    if stage_in.notes:
        sheet.notes = f"{sheet.notes or ''}\n[Stage Update to {stage_in.crop_stage}]: {stage_in.notes}".strip()
    if stage_in.actual_yield_kg is not None:
        sheet.actual_yield_kg = stage_in.actual_yield_kg
    
    db.commit()
    db.refresh(sheet)
    return sheet

@router.delete("/{sheet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_yard_sheet(sheet_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sheet = db.query(YardSheet).filter(YardSheet.id == sheet_id).first()
    if not sheet:
        raise HTTPException(status_code=404, detail="Yard sheet not found")
    if current_user.role != "admin" and sheet.farm.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    db.delete(sheet)
    db.commit()
    return None
