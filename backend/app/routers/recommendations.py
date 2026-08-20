from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from ..database import get_db
from ..models.user import User
from ..models.farm import Farm, SoilRecord
from ..models.advisory import CropRecommendation
from ..schemas.advisory_schema import CropRecommendationRequest, CropRecommendationResponse, CropRecommendationItem
from ..services.auth_service import get_current_user
from ..services.crop_recommendation_engine import recommend_crops

router = APIRouter(prefix="/api/recommendations", tags=["Crop Recommendations"])

@router.post("/generate", response_model=CropRecommendationResponse)
def get_crop_recommendations(req: CropRecommendationRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    params = req.model_dump()
    
    # If farm_id provided, supplement missing params from farm & latest soil record
    if req.farm_id:
        farm = db.query(Farm).filter(Farm.id == req.farm_id).first()
        if farm:
            params["soil_type"] = farm.soil_type
            params["water_availability"] = farm.water_availability
            params["farm_size_acres"] = farm.land_area_acres
            params["state"] = farm.state
            if farm.soil_records:
                latest_soil = sorted(farm.soil_records, key=lambda s: s.created_at, reverse=True)[0]
                params["soil_ph"] = latest_soil.soil_ph
                params["nitrogen_n"] = latest_soil.nitrogen_n
                params["phosphorus_p"] = latest_soil.phosphorus_p
                params["potassium_k"] = latest_soil.potassium_k

    results = recommend_crops(params)

    # Persist recommendation to DB if farm_id is valid
    if req.farm_id:
        for item in results:
            rec_entry = CropRecommendation(
                farm_id=req.farm_id,
                recommended_crop=item["crop_name"],
                suitability_score=item["suitability_score"],
                reason=item["reason"],
                water_requirement=item["water_requirement"],
                fertilizer_advice=item["fertilizer_advice"],
                risk_factors=item["potential_risks"],
                season=params.get("season", "Kharif")
            )
            db.add(rec_entry)
        db.commit()

    return {
        "farm_id": req.farm_id,
        "analysis_date": datetime.utcnow(),
        "environmental_summary": {
            "soil_type": params.get("soil_type"),
            "soil_ph": params.get("soil_ph"),
            "nitrogen_n": params.get("nitrogen_n"),
            "phosphorus_p": params.get("phosphorus_p"),
            "potassium_k": params.get("potassium_k"),
            "season": params.get("season"),
            "water_availability": params.get("water_availability")
        },
        "recommendations": [CropRecommendationItem(**item) for item in results]
    }
