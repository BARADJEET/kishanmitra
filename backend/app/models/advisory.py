from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class CropRecommendation(Base):
    __tablename__ = "crop_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    recommended_crop = Column(String(100), nullable=False)
    suitability_score = Column(Float, nullable=False)  # 0 to 100
    reason = Column(Text, nullable=False)
    water_requirement = Column(String(100), nullable=False)  # Low, Moderate, High
    fertilizer_advice = Column(Text, nullable=True)
    risk_factors = Column(Text, nullable=True)
    season = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    farm = relationship("Farm", back_populates="recommendations")
