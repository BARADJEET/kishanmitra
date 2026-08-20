from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.policy import GovernmentPolicy
from ..schemas.policy_schema import PolicyResponse

router = APIRouter(prefix="/api/policies", tags=["Government Policies & Subsidies"])

@router.get("/", response_model=List[PolicyResponse])
def get_policies(
    state: Optional[str] = None,
    crop: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    q = db.query(GovernmentPolicy)
    if state and state.lower() != "all india":
        q = q.filter(GovernmentPolicy.applicable_state.in_([state, "All India", "National"]))
    if crop:
        q = q.filter(GovernmentPolicy.applicable_crops.ilike(f"%{crop}%") | (GovernmentPolicy.applicable_crops == "All Crops"))
    if category and category.lower() != "all":
        q = q.filter(GovernmentPolicy.category.ilike(f"%{category}%"))
    if search:
        q = q.filter(GovernmentPolicy.title.ilike(f"%{search}%") | GovernmentPolicy.description.ilike(f"%{search}%"))
    return q.order_by(GovernmentPolicy.created_at.desc()).all()

@router.get("/{policy_id}", response_model=PolicyResponse)
def get_policy(policy_id: int, db: Session = Depends(get_db)):
    p = db.query(GovernmentPolicy).filter(GovernmentPolicy.id == policy_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Policy not found")
    return p
