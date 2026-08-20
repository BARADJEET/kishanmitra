from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.disease import DiseasePest, Product, DiseaseSolution
from ..schemas.disease_schema import DiseaseResponse, ProductResponse, DiseaseSolutionResponse

router = APIRouter(prefix="/api/catalog", tags=["Agricultural Catalog"])

@router.get("/diseases", response_model=List[DiseaseResponse])
def list_diseases(crop: Optional[str] = None, search: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(DiseasePest)
    if crop:
        q = q.filter(DiseasePest.target_crops.ilike(f"%{crop}%"))
    if search:
        q = q.filter(DiseasePest.name.ilike(f"%{search}%") | DiseasePest.symptoms.ilike(f"%{search}%"))
    return q.all()

@router.get("/products", response_model=List[ProductResponse])
def list_products(category: Optional[str] = None, crop: Optional[str] = None, search: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(Product)
    if category:
        q = q.filter(Product.category.ilike(f"%{category}%"))
    if crop:
        q = q.filter(Product.suitable_crops.ilike(f"%{crop}%"))
    if search:
        q = q.filter(Product.name.ilike(f"%{search}%") | Product.active_ingredient.ilike(f"%{search}%"))
    return q.all()
