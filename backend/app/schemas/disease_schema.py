from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProductCreate(BaseModel):
    solution_id: Optional[int] = None
    name: str
    category: str
    manufacturer: Optional[str] = None
    active_ingredient: Optional[str] = None
    description: Optional[str] = None
    dosage_instructions: str
    suitable_crops: Optional[str] = None
    price_estimate: Optional[str] = None

class ProductUpdate(BaseModel):
    solution_id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[str] = None
    manufacturer: Optional[str] = None
    active_ingredient: Optional[str] = None
    description: Optional[str] = None
    dosage_instructions: Optional[str] = None
    suitable_crops: Optional[str] = None
    price_estimate: Optional[str] = None

class ProductResponse(ProductCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class DiseaseSolutionResponse(BaseModel):
    id: int
    disease_id: int
    crop_name: str
    recommended_action: str
    organic_treatment: Optional[str] = None
    chemical_treatment: Optional[str] = None
    safety_notes: Optional[str] = None
    products: List[ProductResponse] = []

    class Config:
        from_attributes = True

class DiseaseResponse(BaseModel):
    id: int
    name: str
    scientific_name: Optional[str] = None
    target_crops: str
    symptoms: str
    description: str
    prevention_methods: str
    severity_level: str
    image_sample_url: Optional[str] = None
    solutions: List[DiseaseSolutionResponse] = []

    class Config:
        from_attributes = True

class MLPredictionResponse(BaseModel):
    id: int
    farmer_id: int
    farm_id: Optional[int] = None
    image_url: str
    crop_name: Optional[str] = None
    predicted_disease: str
    confidence_score: float
    symptoms: Optional[str] = None
    recommended_solution: Optional[str] = None
    prevention: Optional[str] = None
    related_products: List[ProductResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True
