from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class Farm(Base):
    __tablename__ = "farms"

    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    farm_name = Column(String(255), nullable=False)
    land_area_acres = Column(Float, nullable=False, default=1.0)
    state = Column(String(100), nullable=False, default="Gujarat")
    district = Column(String(100), nullable=False, default="Ahmedabad")
    village = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=True, default=23.0225)
    longitude = Column(Float, nullable=True, default=72.5714)
    soil_type = Column(String(100), nullable=False, default="Black Soil")  # Alluvial, Black, Red, Clay, Sandy, Laterite
    irrigation_type = Column(String(100), nullable=False, default="Drip")  # Drip, Sprinkler, Flood, Rainfed, Canal
    water_availability = Column(String(50), nullable=False, default="Moderate")  # Abundant, Moderate, Scarce
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    farmer = relationship("User", back_populates="farms")
    soil_records = relationship("SoilRecord", back_populates="farm", cascade="all, delete-orphan")
    yard_sheets = relationship("YardSheet", back_populates="farm", cascade="all, delete-orphan")
    recommendations = relationship("CropRecommendation", back_populates="farm", cascade="all, delete-orphan")

class SoilRecord(Base):
    __tablename__ = "soil_records"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    nitrogen_n = Column(Float, nullable=False, default=60.0)  # kg/ha
    phosphorus_p = Column(Float, nullable=False, default=30.0)  # kg/ha
    potassium_k = Column(Float, nullable=False, default=40.0)  # kg/ha
    soil_ph = Column(Float, nullable=False, default=6.5)
    organic_carbon = Column(Float, nullable=True, default=0.6)  # %
    test_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    farm = relationship("Farm", back_populates="soil_records")
