import os
import uuid
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..config import UPLOAD_DIR
from ..database import get_db
from ..models.user import User
from ..models.disease import MLPrediction, Product
from ..schemas.disease_schema import MLPredictionResponse
from ..services.auth_service import get_current_user
from ..services.ml_vision_service import diagnose_crop_disease

router = APIRouter(prefix="/api/disease-diagnosis", tags=["ML Plant Disease Diagnosis"])

@router.post("/upload", response_model=MLPredictionResponse, status_code=status.HTTP_201_CREATED)
async def upload_crop_image(
    file: UploadFile = File(...),
    farm_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate content type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid image file format. Supported: JPG, PNG, WEBP.")

    # Save image with unique filename
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    unique_filename = f"crop_scan_{uuid.uuid4().hex[:12]}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Perform ML computer vision analysis
    diagnosis = diagnose_crop_disease(file_path)

    # Save prediction record
    pred_record = MLPrediction(
        farmer_id=current_user.id,
        farm_id=farm_id,
        image_url=f"/uploads/{unique_filename}",
        crop_name=diagnosis["crop_name"],
        predicted_disease=diagnosis["predicted_disease"],
        confidence_score=diagnosis["confidence_score"],
        symptoms=diagnosis["symptoms"],
        recommended_solution=f"Immediate: {diagnosis['recommended_solution']}\n\nOrganic: {diagnosis['organic_treatment']}\n\nChemical: {diagnosis['chemical_treatment']}",
        prevention=diagnosis["prevention"]
    )
    db.add(pred_record)
    db.commit()
    db.refresh(pred_record)

    # Fetch matching products if any
    related_products = db.query(Product).filter(
        Product.suitable_crops.ilike(f"%{diagnosis['crop_name'].split(' ')[0]}%")
    ).limit(3).all()

    return {
        "id": pred_record.id,
        "farmer_id": pred_record.farmer_id,
        "farm_id": pred_record.farm_id,
        "image_url": pred_record.image_url,
        "crop_name": pred_record.crop_name,
        "predicted_disease": pred_record.predicted_disease,
        "confidence_score": pred_record.confidence_score,
        "symptoms": pred_record.symptoms,
        "recommended_solution": pred_record.recommended_solution,
        "prevention": pred_record.prevention,
        "related_products": related_products,
        "created_at": pred_record.created_at
    }

@router.get("/history", response_model=List[MLPredictionResponse])
def get_prediction_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == "admin":
        preds = db.query(MLPrediction).order_by(MLPrediction.created_at.desc()).limit(50).all()
    else:
        preds = db.query(MLPrediction).filter(MLPrediction.farmer_id == current_user.id).order_by(MLPrediction.created_at.desc()).all()
    
    return [
        {
            "id": p.id,
            "farmer_id": p.farmer_id,
            "farm_id": p.farm_id,
            "image_url": p.image_url,
            "crop_name": p.crop_name,
            "predicted_disease": p.predicted_disease,
            "confidence_score": p.confidence_score,
            "symptoms": p.symptoms,
            "recommended_solution": p.recommended_solution,
            "prevention": p.prevention,
            "related_products": [],
            "created_at": p.created_at
        }
        for p in preds
    ]
