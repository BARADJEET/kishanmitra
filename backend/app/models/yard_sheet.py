from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from datetime import datetime, date
from ..database import Base

class YardSheet(Base):
    __tablename__ = "yard_sheets"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    crop_name = Column(String(100), nullable=False)
    crop_variety = Column(String(100), nullable=True)
    sowing_date = Column(Date, default=date.today)
    cultivated_area_acres = Column(Float, nullable=False, default=1.0)
    crop_stage = Column(String(50), default="Vegetative")  # Sowing, Germination, Vegetative, Flowering, Fruiting, Harvesting, Post-Harvest
    expected_yield_kg = Column(Float, nullable=True)
    actual_yield_kg = Column(Float, nullable=True)
    season = Column(String(50), default="Kharif")  # Kharif, Rabi, Zaid
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    farm = relationship("Farm", back_populates="yard_sheets")
