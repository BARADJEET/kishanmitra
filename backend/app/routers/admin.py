import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.user import User, UserProfile
from ..models.farm import Farm
from ..models.yard_sheet import YardSheet
from ..models.policy import GovernmentPolicy
from ..models.disease import Product, DiseasePest, DiseaseSolution, MLPrediction
from ..models.audit import AdminAuditLog
from ..schemas.auth_schema import UserResponse
from ..schemas.farm_schema import FarmResponse
from ..schemas.yard_sheet_schema import YardSheetResponse
from ..schemas.policy_schema import PolicyCreate, PolicyUpdate, PolicyResponse
from ..schemas.disease_schema import ProductCreate, ProductUpdate, ProductResponse, DiseaseResponse, MLPredictionResponse
from ..schemas.admin_schema import AdminAuditLogResponse
from ..services.auth_service import require_admin
from ..services.audit_service import log_admin_action

router = APIRouter(prefix="/api/admin", tags=["Admin Operations"], dependencies=[Depends(require_admin)])

# --- 1. Farmers Management ---
@router.get("/farmers", response_model=List[UserResponse])
def get_all_farmers(db: Session = Depends(get_db)):
    return db.query(User).filter(User.role == "farmer").all()

@router.patch("/farmers/{user_id}/status", response_model=UserResponse)
def toggle_farmer_status(user_id: int, is_active: bool, current_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    old_val = {"is_active": user.is_active}
    user.is_active = is_active
    db.commit()
    db.refresh(user)

    log_admin_action(
        db=db,
        admin=current_admin,
        entity_type="User",
        entity_id=user.id,
        action="UPDATE",
        description=f"Admin toggled farmer {user.email} status to is_active={is_active}",
        old_values=old_val,
        new_values={"is_active": user.is_active}
    )
    return user

# --- 2. Policies CRUD ---
@router.post("/policies", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
def create_policy(policy_in: PolicyCreate, current_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    new_pol = GovernmentPolicy(**policy_in.model_dump())
    db.add(new_pol)
    db.commit()
    db.refresh(new_pol)

    log_admin_action(
        db=db,
        admin=current_admin,
        entity_type="GovernmentPolicy",
        entity_id=new_pol.id,
        action="CREATE",
        description=f"Created government scheme: {new_pol.title}",
        new_values=policy_in.model_dump()
    )
    return new_pol

@router.put("/policies/{policy_id}", response_model=PolicyResponse)
def update_policy(policy_id: int, policy_in: PolicyUpdate, current_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    pol = db.query(GovernmentPolicy).filter(GovernmentPolicy.id == policy_id).first()
    if not pol:
        raise HTTPException(status_code=404, detail="Policy not found")

    old_vals = {c.name: getattr(pol, c.name) for c in pol.__table__.columns if c.name not in ["created_at", "updated_at"]}
    for k, v in policy_in.model_dump(exclude_unset=True).items():
        setattr(pol, k, v)
    db.commit()
    db.refresh(pol)

    log_admin_action(
        db=db,
        admin=current_admin,
        entity_type="GovernmentPolicy",
        entity_id=pol.id,
        action="UPDATE",
        description=f"Updated government scheme: {pol.title}",
        old_values=old_vals,
        new_values=policy_in.model_dump(exclude_unset=True)
    )
    return pol

@router.delete("/policies/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_policy(policy_id: int, current_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    pol = db.query(GovernmentPolicy).filter(GovernmentPolicy.id == policy_id).first()
    if not pol:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    old_title = pol.title
    db.delete(pol)
    db.commit()

    log_admin_action(
        db=db,
        admin=current_admin,
        entity_type="GovernmentPolicy",
        entity_id=policy_id,
        action="DELETE",
        description=f"Deleted government scheme: {old_title}"
    )
    return None

# --- 3. Products CRUD ---
@router.post("/products", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, current_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    new_prod = Product(**product_in.model_dump())
    db.add(new_prod)
    db.commit()
    db.refresh(new_prod)

    log_admin_action(
        db=db,
        admin=current_admin,
        entity_type="Product",
        entity_id=new_prod.id,
        action="CREATE",
        description=f"Added agricultural product: {new_prod.name} ({new_prod.category})",
        new_values=product_in.model_dump()
    )
    return new_prod

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_in: ProductUpdate, current_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")

    old_vals = {c.name: getattr(prod, c.name) for c in prod.__table__.columns if c.name not in ["created_at", "updated_at"]}
    for k, v in product_in.model_dump(exclude_unset=True).items():
        setattr(prod, k, v)
    db.commit()
    db.refresh(prod)

    log_admin_action(
        db=db,
        admin=current_admin,
        entity_type="Product",
        entity_id=prod.id,
        action="UPDATE",
        description=f"Updated agricultural product: {prod.name}",
        old_values=old_vals,
        new_values=product_in.model_dump(exclude_unset=True)
    )
    return prod

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, current_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    prod = db.query(Product).filter(Product.id == product_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    
    name = prod.name
    db.delete(prod)
    db.commit()

    log_admin_action(
        db=db,
        admin=current_admin,
        entity_type="Product",
        entity_id=product_id,
        action="DELETE",
        description=f"Deleted agricultural product: {name}"
    )
    return None

# --- 4. Admin Audit Logs ---
@router.get("/audit-logs", response_model=List[AdminAuditLogResponse])
def get_audit_logs(db: Session = Depends(get_db)):
    return db.query(AdminAuditLog).order_by(AdminAuditLog.created_at.desc()).limit(100).all()
